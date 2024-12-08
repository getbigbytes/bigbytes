from bigbytes.data_preparation.models.constants import BlockType
from bigbytes.frameworks.execution.llm.rag.pipelines.data_preparation import (
    DATA_PREPARATION,
)
from bigbytes.frameworks.execution.llm.rag.pipelines.inference import INFERENCE
from bigbytes.frameworks.execution.models.block.base import BlockExecutionFramework
from bigbytes.frameworks.execution.models.enums import ExecutionFrameworkUUID
from bigbytes.frameworks.execution.models.pipeline.base import PipelineExecutionFramework

RAG = PipelineExecutionFramework.load(
    uuid=ExecutionFrameworkUUID.RAG,
    description=(
        'A powerful system that efficiently processes large amounts of data and generates '
        'highly relevant responses to complex user queries by leveraging advanced techniques '
        'in natural language processing, information retrieval, and machine learning'
    ),
    blocks=[
        BlockExecutionFramework.load(
            uuid=DATA_PREPARATION.uuid,
            description=DATA_PREPARATION.description,
            type=BlockType.PIPELINE,
        ),
        BlockExecutionFramework.load(
            uuid=INFERENCE.uuid,
            description=INFERENCE.description,
            type=BlockType.PIPELINE,
        ),
    ],
    pipelines=[
        DATA_PREPARATION,
        INFERENCE,
    ],
)
