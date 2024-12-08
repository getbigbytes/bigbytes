from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.EventRulePresenter import EventRulePresenter
from bigbytes.orchestration.constants import Entity


class EventRulePolicy(BasePolicy):
    @property
    def entity(self):
        return Entity.ANY, None


EventRulePolicy.allow_actions([
    constants.DETAIL,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

EventRulePolicy.allow_read(EventRulePresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
], condition=lambda policy: policy.has_at_least_viewer_role())
