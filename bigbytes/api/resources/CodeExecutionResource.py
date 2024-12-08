from datetime import datetime

from bigbytes.api.errors import ApiError
from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.kernels.magic.kernels.manager import KernelManager
from bigbytes.shared.environments import is_debug


class CodeExecutionResource(GenericResource):
    @classmethod
    async def create(cls, payload, user, **kwargs) -> GenericResource:
        now = datetime.utcnow().timestamp()
        if is_debug():
            print('[CodeExecutionResource.create]', now)

        message = payload.get('message', '')
        message_request_uuid = payload.get('message_request_uuid')
        num_processes = payload.get('num_processes', None)
        uuid = payload.get('uuid')

        if uuid is None:
            error = ApiError(ApiError.RESOURCE_INVALID)
            error.message = 'UUID is required'
            raise error

        kernel = KernelManager.get_kernel(uuid, num_processes=num_processes)
        process = kernel.run(
            message,
            message_request_uuid=message_request_uuid,
            timestamp=now,
        )

        if is_debug():
            print(f'[CodeExecutionResource.create] Process {process.message_uuid} started')
        return cls(process, user, **kwargs)
