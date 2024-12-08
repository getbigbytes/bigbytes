from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.api.resources.mixins.spark import SparkApplicationChild
from bigbytes.services.spark.models.executors import Executor


class SparkExecutorResource(GenericResource, SparkApplicationChild):
    @classmethod
    async def collection(self, _query, _meta, user, **kwargs):
        application_id = await self.get_application_id(**kwargs)

        return self.build_result_set(
            await self.build_api().executors(application_id=application_id),
            user,
            **kwargs,
        )

    @classmethod
    async def get_model(self, pk, **kwargs) -> Executor:
        return Executor.load(id=pk)
