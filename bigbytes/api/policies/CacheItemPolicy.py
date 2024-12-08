from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.CacheItemPresenter import CacheItemPresenter


class CacheItemPolicy(BasePolicy):
    pass


CacheItemPolicy.allow_actions(
    [
        constants.DETAIL,
        constants.LIST,
        constants.UPDATE,
    ],
    scopes=[OauthScope.CLIENT_PRIVATE],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)


CacheItemPolicy.allow_read(
    CacheItemPresenter.default_attributes + [],
    scopes=[OauthScope.CLIENT_PRIVATE],
    on_action=[
        constants.DETAIL,
        constants.LIST,
        constants.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)


CacheItemPolicy.allow_query(
    [
        'item_type',
        'project_path',
    ],
    scopes=[OauthScope.CLIENT_PRIVATE],
    on_action=[
        constants.DETAIL,
        constants.LIST,
        constants.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)
