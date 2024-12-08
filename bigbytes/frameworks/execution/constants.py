from bigbytes.frameworks.execution.llm.rag.base import RAG
from bigbytes.frameworks.execution.models.enums import ExecutionFrameworkUUID

EXECUTION_FRAMEWORKS = [
    RAG,
]

EXECUTION_FRAMEWORKS_BY_UUID = {
    ExecutionFrameworkUUID.RAG: RAG,
}
