from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.ClusterPresenter import ClusterPresenter
from bigbytes.orchestration.constants import Entity


class ClusterPolicy(BasePolicy):
    @property
    def entity(self):
        return Entity.ANY, None


ClusterPolicy.allow_actions([
    constants.DETAIL,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

ClusterPolicy.allow_actions([
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_editor_role())

ClusterPolicy.allow_read(ClusterPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

ClusterPolicy.allow_write([
    'id',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_editor_role())
