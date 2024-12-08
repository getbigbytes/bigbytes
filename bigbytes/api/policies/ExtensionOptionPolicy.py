from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.ExtensionOptionPresenter import ExtensionOptionPresenter
from bigbytes.orchestration.constants import Entity


class ExtensionOptionPolicy(BasePolicy):
    @property
    def entity(self):
        return Entity.ANY, None


ExtensionOptionPolicy.allow_actions([
    constants.DETAIL,
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


ExtensionOptionPolicy.allow_read(ExtensionOptionPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())
