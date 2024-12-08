import asyncio

from bigbytes.authentication.permissions.seed import bootstrap_permissions
from bigbytes.orchestration.db import db_connection

if __name__ == '__main__':
    db_connection.start_session()

    asyncio.run(bootstrap_permissions())
