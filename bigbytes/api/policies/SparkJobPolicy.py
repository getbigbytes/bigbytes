from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.SparkJobPresenter import SparkJobPresenter


class SparkJobPolicy(BasePolicy):
    pass


SparkJobPolicy.allow_actions(
    [
        OperationType.DETAIL,
        OperationType.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)


SparkJobPolicy.allow_read(
    SparkJobPresenter.default_attributes,
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.DETAIL,
        OperationType.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)

SparkJobPolicy.allow_query(
    [
        'application_id',
        'application_spark_ui_url',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        OperationType.DETAIL,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)
