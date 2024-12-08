from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.UserRolePresenter import UserRolePresenter


class UserRolePolicy(BasePolicy):
    pass


UserRolePolicy.allow_actions([
    constants.CREATE,
    constants.DELETE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_admin_role())


UserRolePolicy.allow_read(UserRolePresenter.default_attributes + [
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
    constants.DELETE,
], condition=lambda policy: policy.has_at_least_admin_role())


UserRolePolicy.allow_write([
    'role_id',
    'user_id',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_admin_role())
