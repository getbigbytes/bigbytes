import asyncio
from collections import defaultdict
from datetime import datetime
from typing import cast
from uuid import uuid4

import simplejson

from bigbytes.kernels.magic.constants import EventStreamType
from bigbytes.kernels.magic.models import EventStream
from bigbytes.kernels.magic.queues.manager import get_execution_result_queue_async
from bigbytes.server.api.base import BaseHandler
from bigbytes.shared.parsers import encode_complex
from bigbytes.shared.queues import Empty
from bigbytes.shared.queues import Queue as FasterQueue

SLEEP_SECONDS = 0.1


class EventStreamHandler(BaseHandler):
    active_connections = defaultdict(list)
    consecutive_sleep_count = defaultdict(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = None

    async def get(self, uuid: str) -> None:
        self.uuid = uuid
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')

        while True:
            queue = await self.__get_queue()
            result = None

            try:
                result = queue.get_nowait()  # Non-blocking get
            except Empty:
                pass

            if result is not None:
                event_stream = EventStream.load(
                    event_uuid=uuid4().hex,
                    result=result,
                    timestamp=int(datetime.utcnow().timestamp() * 1000),
                    type=EventStreamType.EXECUTION,
                    uuid=self.uuid,
                )
                event_stream_json = simplejson.dumps(
                    event_stream,
                    default=encode_complex,
                    ignore_nan=True,
                )
                self.write(f'data: {event_stream_json}\n\n')

            await self.flush()
            await asyncio.sleep(SLEEP_SECONDS)

    async def __get_queue(self) -> FasterQueue:
        kernel_queue = await get_execution_result_queue_async()
        return cast(dict, kernel_queue)[self.uuid]
