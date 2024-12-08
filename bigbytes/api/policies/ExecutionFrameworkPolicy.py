from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.ExecutionFrameworkPresenter import (
    ExecutionFrameworkPresenter,
)
from bigbytes.orchestration.constants import Entity


class ExecutionFrameworkPolicy(BasePolicy):
    @property
    def entity(self):
        # Adjust the entity to reflect the KernelProcess's entity, if applicable
        return Entity.ANY, None


ExecutionFrameworkPolicy.allow_actions(
    [
        OperationType.DETAIL,
        OperationType.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)


ExecutionFrameworkPolicy.allow_read(
    ExecutionFrameworkPresenter.default_attributes,
    on_action=[
        OperationType.DETAIL,
        OperationType.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

ExecutionFrameworkPolicy.allow_query(
    [
        'level',
    ],
    on_action=[
        OperationType.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)
