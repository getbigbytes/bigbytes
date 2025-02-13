import posixpath
from contextlib import redirect_stdout
from typing import Dict

from bigbytes.data_preparation.executors.block_executor import BlockExecutor
from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.data_preparation.shared.stream import StreamToLogger
from bigbytes.data_preparation.templates.utils import template_env
from bigbytes.services.aws.emr import emr
from bigbytes.services.aws.emr.config import EmrConfig
from bigbytes.services.aws.emr.resource_manager import EmrResourceManager
from bigbytes.services.aws.s3 import s3
from bigbytes.shared.hash import merge_dict


class PySparkBlockExecutor(BlockExecutor):
    def __init__(
        self,
        pipeline: Pipeline,
        block_uuid: str,
        execution_partition: str = None,
        **kwargs,
    ):
        super().__init__(pipeline, block_uuid, execution_partition=execution_partition)
        self.resource_manager = EmrResourceManager(
            pipeline.repo_config.s3_bucket,
            pipeline.repo_config.s3_path_prefix,
        )
        self.s3_bucket = pipeline.repo_config.s3_bucket
        self.s3_path_prefix = pipeline.repo_config.s3_path_prefix
        self.executor_config = self.pipeline.repo_config.emr_config
        if self.pipeline.executor_config is not None:
            self.executor_config = merge_dict(self.executor_config, self.pipeline.executor_config)
        if self.block.executor_config is not None:
            self.executor_config = merge_dict(self.executor_config, self.block.executor_config)
        self.executor_config = EmrConfig.load(config=self.executor_config)

    def _execute(
        self,
        analyze_outputs: bool = False,
        global_vars: Dict = None,
        update_status: bool = False,
        **kwargs,
    ) -> None:
        """
        Run block in a spark cluster
        1. Upload block execution script to S3
        2. Launch or connect to an EMR spark cluster
        3. Submit a spark job
        """
        stdout = StreamToLogger(self.logger)
        with redirect_stdout(stdout):
            self.upload_block_execution_script(global_vars=global_vars)
            self.resource_manager.upload_bootstrap_script()
            self.submit_spark_job()

    @property
    def spark_script_path(self) -> str:
        return posixpath.join('s3://', self.s3_bucket, self.spark_script_path_key)

    @property
    def spark_script_path_key(self) -> str:
        return posixpath.join(
            self.s3_path_prefix,
            f'scripts/{self.pipeline.uuid}/{self.block_uuid}.py',
        )

    def upload_block_execution_script(self, global_vars: Dict = None) -> None:
        execution_script_code = template_env.get_template(
            'pipeline_execution/spark_script.jinja',
        ).render(
            block_uuid=f'\'{self.block_uuid}\'',
            execution_partition_str=f'\'{self.execution_partition}\''
                                    if self.execution_partition is not None else None,
            global_vars=global_vars,
            pipeline_config=self.pipeline.to_dict(include_content=True),
            pipeline_uuid=self.pipeline.uuid,
            repo_config=self.pipeline.repo_config.to_dict(remote=True),
            spark_log_path=self.resource_manager.log_uri,
        )

        s3.Client(self.s3_bucket).upload(self.spark_script_path_key, execution_script_code)

    def submit_spark_job(self):
        step = {
            'name': f'run_mage_block_{self.pipeline.uuid}_{self.block_uuid}',
            'jars': self.executor_config.spark_jars,
            'script_uri': self.spark_script_path,
            'script_args': [],
        }
        return emr.submit_spark_job(
            cluster_name=step['name'],
            steps=[step],
            bootstrap_script_path=self.resource_manager.bootstrap_script_path,
            emr_config=self.executor_config,
            log_uri=self.resource_manager.log_uri,
        )
