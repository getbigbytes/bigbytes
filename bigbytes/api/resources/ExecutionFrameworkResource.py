from typing import List, Optional, Union

from bigbytes.api.errors import ApiError
from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.api.resources.PipelineExecutionFrameworkResource import (
    PipelineExecutionFrameworkResource,
)
from bigbytes.frameworks.execution.constants import EXECUTION_FRAMEWORKS
from bigbytes.frameworks.execution.models.pipeline.base import PipelineExecutionFramework
from bigbytes.shared.array import find


def get_execution_frameworks(
    level: Optional[int] = None,
    uuid: Optional[str] = None,
) -> Union[List[PipelineExecutionFramework], PipelineExecutionFramework]:
    arr = []
    for framework in EXECUTION_FRAMEWORKS:
        arr.append(framework)
        if level is None or level >= 1:
            arr += framework.get_pipelines(level=level)

    if uuid:
        result = find(lambda framework: framework.uuid == uuid, arr)
        if result:
            return result
        else:
            raise ApiError(ApiError.RESOURCE_NOT_FOUND)
    return arr


class ExecutionFrameworkResource(GenericResource):
    @classmethod
    async def collection(cls, query, meta, user, **kwargs):
        level = query.get('level', [None])
        if level:
            level = level[0]
        if level is not None:
            level = int(level)

        return cls.build_result_set(
            get_execution_frameworks(level=level),
            user,
            **kwargs,
        )

    @classmethod
    async def get_model(cls, pk, **kwargs) -> PipelineExecutionFramework:
        model = get_execution_frameworks(uuid=pk)
        if isinstance(model, list):
            return model[0]
        return model

    @classmethod
    async def member(cls, pk, user, **kwargs):
        model = cls.get_model(pk, **kwargs)

        if not model:
            raise ApiError(ApiError.RESOURCE_NOT_FOUND)

        return cls(model, user, **kwargs)


ExecutionFrameworkResource.register_child_resource('pipelines', PipelineExecutionFrameworkResource)
