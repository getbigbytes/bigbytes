from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.PageBlockLayoutPresenter import PageBlockLayoutPresenter


class PageBlockLayoutPolicy(BasePolicy):
    pass


PageBlockLayoutPolicy.allow_actions([
    constants.DETAIL,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


PageBlockLayoutPolicy.allow_actions([
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_editor_role())


PageBlockLayoutPolicy.allow_read(PageBlockLayoutPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
], condition=lambda policy: policy.has_at_least_viewer_role())


PageBlockLayoutPolicy.allow_read(PageBlockLayoutPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_editor_role())


PageBlockLayoutPolicy.allow_write([
    'blocks',
    'layout',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_editor_role())
