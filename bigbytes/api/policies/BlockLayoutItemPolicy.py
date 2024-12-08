from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.BlockLayoutItemPresenter import BlockLayoutItemPresenter


class BlockLayoutItemPolicy(BasePolicy):
    pass


BlockLayoutItemPolicy.allow_actions([
    constants.DETAIL,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


BlockLayoutItemPolicy.allow_read(BlockLayoutItemPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
], condition=lambda policy: policy.has_at_least_viewer_role())


BlockLayoutItemPolicy.allow_query(scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
], condition=lambda policy: policy.has_at_least_viewer_role())
