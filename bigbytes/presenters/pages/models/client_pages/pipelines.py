from bigbytes.api.operations.constants import OperationType
from bigbytes.presenters.pages.models.base import ClientPage
from bigbytes.presenters.pages.models.constants import ResourceType


class BasePage(ClientPage):
    resource = ResourceType.PIPELINE
    version = 1


class ListPage(BasePage):
    operation = OperationType.LIST


class DetailPage(BasePage):
    operation = OperationType.DETAIL
