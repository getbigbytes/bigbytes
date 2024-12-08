from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.SparkExecutorPresenter import SparkExecutorPresenter


class SparkExecutorPolicy(BasePolicy):
    pass


SparkExecutorPolicy.allow_actions(
    [
        OperationType.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)


SparkExecutorPolicy.allow_read(
    SparkExecutorPresenter.default_attributes,
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)
