from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.ConfigurationOptionPresenter import (
    ConfigurationOptionPresenter,
)


class ConfigurationOptionPolicy(BasePolicy):
    pass


ConfigurationOptionPolicy.allow_actions(
    [constants.LIST],
    scopes=[OauthScope.CLIENT_PRIVATE],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)


ConfigurationOptionPolicy.allow_read(
    ConfigurationOptionPresenter.default_attributes + [],
    scopes=[OauthScope.CLIENT_PRIVATE],
    on_action=[constants.LIST],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)


ConfigurationOptionPolicy.allow_query(
    [
        'configuration_type',
        'option_type',
        'resource_type',
        'resource_uuid',
    ],
    scopes=[OauthScope.CLIENT_PRIVATE],
    on_action=[constants.LIST],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)
