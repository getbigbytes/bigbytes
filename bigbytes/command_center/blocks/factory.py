import asyncio
from datetime import datetime
from typing import Dict, List

from bigbytes.cache.block import BlockCache
from bigbytes.command_center.blocks.utils import add_application_actions, build_and_score
from bigbytes.command_center.factory import BaseFactory
from bigbytes.shared.hash import merge_dict


class BlockFactory(BaseFactory):
    async def fetch_items(self, **kwargs) -> List[Dict]:
        items = []

        if self.search:
            now = datetime.utcnow().timestamp()
            cache = await BlockCache.initialize_cache()
            mapping = cache.get(cache.cache_key)
            print(f'[BlockFactory] Load: {len(mapping)} - {datetime.utcnow().timestamp() - now}')

            data_array = mapping.items()
            now = datetime.utcnow().timestamp()
            await asyncio.gather(
                *[build_and_score(self, data, items) for data in data_array]
            )
            print(
                f'[BlockFactory] Search {self.search}: '
                f'{len(items)} - {datetime.utcnow().timestamp() - now}',
            )

            now = datetime.utcnow().timestamp()
            items = await self.rank_items(items)
            items = [merge_dict(
                item_dict,
                add_application_actions(item_dict),
            ) for item_dict in items]
            print(f'[BlockFactory] Rank items: {datetime.utcnow().timestamp() - now}')

        return items
