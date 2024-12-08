from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.IntegrationSourceStreamPresenter import IntegrationSourceStreamPresenter


class IntegrationSourceStreamPolicy(BasePolicy):
    pass


IntegrationSourceStreamPolicy.allow_actions([
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

IntegrationSourceStreamPolicy.allow_read(IntegrationSourceStreamPresenter.default_attributes + [
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_viewer_role())
