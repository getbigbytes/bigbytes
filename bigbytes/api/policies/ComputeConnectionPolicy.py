from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.ComputeConnectionPresenter import ComputeConnectionPresenter


class ComputeConnectionPolicy(BasePolicy):
    pass


ComputeConnectionPolicy.allow_actions(
    [
        OperationType.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)


ComputeConnectionPolicy.allow_actions(
    [
        OperationType.UPDATE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
    override_permission_condition=lambda _policy: True,
)


ComputeConnectionPolicy.allow_read(
    ComputeConnectionPresenter.default_attributes,
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)


ComputeConnectionPolicy.allow_read(
    ComputeConnectionPresenter.default_attributes,
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
    override_permission_condition=lambda _policy: True,
)


ComputeConnectionPolicy.allow_write(
    [
        'action',
        'connection',
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
