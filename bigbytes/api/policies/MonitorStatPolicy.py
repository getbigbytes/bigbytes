from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.MonitorStatPresenter import MonitorStatPresenter


class MonitorStatPolicy(BasePolicy):
    pass


MonitorStatPolicy.allow_actions([
    constants.DETAIL,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

MonitorStatPolicy.allow_read([] + MonitorStatPresenter.default_attributes, scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
], condition=lambda policy: policy.has_at_least_viewer_role())

MonitorStatPolicy.allow_query([
    'end_time',
    'group_by_pipeline_type',
    'pipeline_schedule_id',
    'pipeline_uuid',
    'start_time',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())
