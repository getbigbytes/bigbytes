import urllib.parse

from bigbytes.api.errors import ApiError
from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.cache.block_action_object import BlockActionObjectCache
from bigbytes.data_preparation.models.block import Block
from bigbytes.data_preparation.models.errors import FileNotInProjectError
from bigbytes.data_preparation.models.file import File, ensure_file_is_in_project
from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.orchestration.db import safe_db_query
from bigbytes.settings.repo import get_repo_path
from bigbytes.shared.array import find
from bigbytes.shared.path_fixer import add_absolute_path


class FileContentResource(GenericResource):
    @classmethod
    @safe_db_query
    async def member(self, pk, user, **kwargs):
        file = None

        if 'payload' in kwargs and 'file_content' in kwargs['payload']:
            payload = kwargs['payload']['file_content']
            if 'block_uuid' in payload and 'pipeline_uuid' in payload:
                repo_path = get_repo_path(user=user)
                pipeline = await Pipeline.get_async(
                    payload.get('pipeline_uuid'), repo_path=repo_path
                )
                if pipeline:
                    block = pipeline.get_block(payload.get('block_uuid'))
                    if block:
                        file = block.file

        if not file:
            file_path = urllib.parse.unquote(pk)
            file = File.from_path(add_absolute_path(file_path), get_repo_path(root_project=True))

        try:
            ensure_file_is_in_project(file.file_path)
        except FileNotInProjectError:
            error = ApiError.RESOURCE_INVALID.copy()
            error.update(
                message=f'File at path: {file.file_path} is not in the project directory.')
            raise ApiError(error)
        return self(file, user, **kwargs)

    async def update(self, payload, **kwargs):
        error = ApiError.RESOURCE_INVALID.copy()

        content = payload.get('content')
        version = payload.get('version')

        if content is None and version is None:
            error.update(message='Please provide a content or version in the request payload.')
            raise ApiError(error)

        if version is not None and content is None:
            file_version = find(lambda f: f.filename == str(version), self.model.file_versions())
            content = file_version.content()

        await self.model.update_content_async(content)

        block_type = Block.block_type_from_path(
            self.model.dir_path,
            repo_path=get_repo_path(user=self.current_user),
        )
        if block_type:
            cache_block_action_object = await BlockActionObjectCache.initialize_cache()
            cache_block_action_object.update_block(block_file_absolute_path=self.model.file_path)
