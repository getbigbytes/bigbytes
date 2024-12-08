import aiohttp

from bigbytes.server.api.base import BaseHandler
from bigbytes.server.constants import VERSION
from bigbytes.settings.repo import get_repo_path


class ApiProjectsHandler(BaseHandler):
    async def get(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://pypi.org/pypi/bigbytes/json',
                    timeout=3,
                ) as response:
                    response_json = await response.json()
                    latest_version = response_json.get('info', {}).get('version', None)
        except Exception:
            latest_version = VERSION
        parts = get_repo_path().split('/')
        collection = [
            dict(
                latest_version=latest_version,
                name=parts[-1],
                version=VERSION,
            ),
        ]
        self.write(dict(projects=collection))
