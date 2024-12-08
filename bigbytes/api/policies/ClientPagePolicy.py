from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.ClientPagePresenter import ClientPagePresenter


class ClientPagePolicy(BasePolicy):
    pass


ClientPagePolicy.allow_actions([
    constants.CREATE,
    constants.DETAIL,
    constants.LIST,
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


ClientPagePolicy.allow_read(ClientPagePresenter.default_attributes + [
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())


ClientPagePolicy.allow_read(ClientPagePresenter.default_attributes + [
    'components',
    'metadata',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
    constants.DETAIL,
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


ClientPagePolicy.allow_write([
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


ClientPagePolicy.allow_query([
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())
