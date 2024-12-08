from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.VersionControlFilePresenter import (
    VersionControlFilePresenter,
)


class VersionControlFilePolicy(BasePolicy):
    pass


VersionControlFilePolicy.allow_actions(
    [
        OperationType.CREATE,
        OperationType.DELETE,
        OperationType.DETAIL,
        OperationType.LIST,
        OperationType.UPDATE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
    override_permission_condition=lambda _policy: True,
)


VersionControlFilePolicy.allow_read(
    VersionControlFilePresenter.default_attributes + [],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.CREATE,
        OperationType.DELETE,
        OperationType.DETAIL,
        OperationType.LIST,
        OperationType.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
    override_permission_condition=lambda _policy: True,
)


VersionControlFilePolicy.allow_write(
    [
        'name',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.CREATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
    override_permission_condition=lambda _policy: True,
)


VersionControlFilePolicy.allow_write(
    [
        'add',
        'command',
        'commit',
        'message',
        'reset',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
    override_permission_condition=lambda _policy: True,
)

VersionControlFilePolicy.allow_query(
    [
        'diff',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.LIST,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
    override_permission_condition=lambda _policy: True,
)
