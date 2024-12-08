from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.SparkEnvironmentPresenter import SparkEnvironmentPresenter


class SparkEnvironmentPolicy(BasePolicy):
    pass


SparkEnvironmentPolicy.allow_actions(
    [
        OperationType.DETAIL,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)


SparkEnvironmentPolicy.allow_read(
    SparkEnvironmentPresenter.default_attributes,
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.DETAIL,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)
