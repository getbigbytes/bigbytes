from dataclasses import dataclass

from bigbytes.cache.constants import CacheItemType
from bigbytes.cache.models import CacheItem


@dataclass
class DBTCacheItem(CacheItem):
    def __post_init__(self):
        super().__post_init__()

        self.item_type = CacheItemType.DBT

        if not self.uuid and self.item and self.item.get('project'):
            self.uuid = (self.item.get('project') or {}).get('uuid')
