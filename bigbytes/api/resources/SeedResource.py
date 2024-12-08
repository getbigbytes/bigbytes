import asyncio
import threading

from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.authentication.permissions.seed import bootstrap_permissions


class SeedResource(GenericResource):
    @classmethod
    async def create(self, payload, user, **kwargs):
        if payload.get('roles') and payload.get('permissions'):
            policy_names = payload.get('policy_names')
            t = threading.Thread(
                target=asyncio.run,
                args=(bootstrap_permissions(policy_names=policy_names),),
            )
            t.start()

        return self({}, user, **kwargs)
