from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.server.api.base import BaseHandler
from bigbytes.settings.repo import get_repo_path


class ApiPipelineBlockAnalysisHandler(BaseHandler):
    def get(self, pipeline_uuid, block_uuid):
        pipeline = Pipeline.get(pipeline_uuid, repo_path=get_repo_path())
        block = pipeline.get_block(block_uuid)
        if block is None:
            raise Exception(f'Block {block_uuid} does not exist in pipeline {pipeline_uuid}')
        analyses = block.get_analyses()
        self.write(dict(analyses=analyses))
