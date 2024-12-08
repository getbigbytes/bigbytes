from typing import List

from bigbytes.command_center.applications.factory import ApplicationFactory
from bigbytes.command_center.blocks.factory import BlockFactory
from bigbytes.command_center.factory import BaseFactory
from bigbytes.command_center.files.factory import FileFactory
from bigbytes.command_center.models import Item
from bigbytes.command_center.pipelines.factory import PipelineFactory
from bigbytes.command_center.support.constants import ITEMS as ITEMS_SUPPORT
from bigbytes.command_center.triggers.factory import TriggerFactory
from bigbytes.command_center.version_control.factory import VersionControlFactory

FACTORIES_OR_ITEMS = [
    ApplicationFactory,
    BlockFactory,
    FileFactory,
    ITEMS_SUPPORT,
    PipelineFactory,
    TriggerFactory,
    VersionControlFactory,
]


async def search_items(**kwargs) -> List[Item]:
    return await BaseFactory.create_items(FACTORIES_OR_ITEMS, **kwargs)
