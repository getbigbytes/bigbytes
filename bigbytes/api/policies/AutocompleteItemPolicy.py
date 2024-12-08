from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.AutocompleteItemPresenter import AutocompleteItemPresenter
from bigbytes.orchestration.constants import Entity


class AutocompleteItemPolicy(BasePolicy):
    @property
    def entity(self):
        return Entity.ANY, None


AutocompleteItemPolicy.allow_actions([
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

AutocompleteItemPolicy.allow_read(AutocompleteItemPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())
