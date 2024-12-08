from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.IntegrationDestinationPresenter import IntegrationDestinationPresenter


class IntegrationDestinationPolicy(BasePolicy):
    pass


IntegrationDestinationPolicy.allow_actions([
    constants.CREATE,
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

IntegrationDestinationPolicy.allow_read(IntegrationDestinationPresenter.default_attributes + [
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())

IntegrationDestinationPolicy.allow_read([
    'error_message',
    'success',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

IntegrationDestinationPolicy.allow_write([
    'action_type',
    'config',
    'pipeline_uuid',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_viewer_role())
