from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.SchedulerPresenter import SchedulerPresenter


class SchedulerPolicy(BasePolicy):
    pass


SchedulerPolicy.allow_actions([
    constants.CREATE,
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

SchedulerPolicy.allow_read(SchedulerPresenter.default_attributes, scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())

SchedulerPolicy.allow_write(['action_type'], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_viewer_role())
