from typing import List

from bigbytes.api.errors import ApiError
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.resources.PipelineScheduleResource import PipelineScheduleResource
from bigbytes.orchestration.db.models.oauth import User
from bigbytes.presenters.pages.models.base import ClientPage, PageComponent
from bigbytes.presenters.pages.models.client_pages.pipelines import (
    DetailPage as PipelinesDetailPage,
)
from bigbytes.presenters.pages.models.constants import ResourceType
from bigbytes.presenters.pages.models.page_components.pipeline_schedules import (
    CreateWithInteractionsComponent,
    EditComponent,
)


class BasePage(ClientPage):
    parent_page: PipelinesDetailPage
    resource = ResourceType.PIPELINE_SCHEDULE
    version = 1


class ListPage(BasePage):
    operation = OperationType.LIST


class CreatePage(BasePage):
    operation = OperationType.CREATE

    @classmethod
    async def components(self, **kwargs) -> List[PageComponent]:
        return [
            CreateWithInteractionsComponent,
            EditComponent,
        ]

    @classmethod
    async def disabled(self, current_user: User = None, **kwargs) -> bool:
        pipelines = kwargs.get('pipelines') or []
        for pipeline in [p for p in pipelines if p]:
            pipeline_schedule = PipelineScheduleResource.model_class(pipeline_uuid=pipeline.uuid)
            resource = PipelineScheduleResource(pipeline_schedule, current_user)
            policy = resource.policy_class()(resource, current_user)
            try:
                await policy.authorize_action(OperationType.CREATE)
            except ApiError:
                return True

        return False
