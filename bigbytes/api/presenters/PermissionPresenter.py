from typing import List

from bigbytes.api.operations import constants
from bigbytes.api.presenters.BasePresenter import BasePresenter
from bigbytes.authentication.permissions.constants import (
    BlockEntityType,
    EntityName,
    PipelineEntityType,
)


class PermissionPresenter(BasePresenter):
    default_attributes = [
        'access',
        'created_at',
        'entity',
        'entity_id',
        'entity_name',
        'entity_type',
        'id',
        'updated_at',
    ]

    def entity_names(self, **kwargs) -> List[str]:
        return sorted([n for n in EntityName])

    def entity_types(self, **kwargs) -> List[str]:
        return sorted(
            [n for n in BlockEntityType] + [n for n in PipelineEntityType],
        )


PermissionPresenter.register_format(
    f'role/{constants.DETAIL}',
    PermissionPresenter.default_attributes + [
        'conditions',
        'query_attributes',
        'read_attributes',
        'write_attributes',
    ],
)


PermissionPresenter.register_formats([
    constants.CREATE,
    constants.DELETE,
    constants.DETAIL,
    constants.UPDATE,
], PermissionPresenter.default_attributes + [
    'conditions',
    'entity_names',
    'entity_types',
    'query_attributes',
    'read_attributes',
    'role',
    'roles',
    'user',
    'user_id',
    'users',
    'write_attributes',
])


PermissionPresenter.register_formats([
    'with_only_entity_options',
], [
    'entity_names',
    'entity_types',
])
