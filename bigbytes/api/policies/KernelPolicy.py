from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.KernelPresenter import KernelPresenter
from bigbytes.orchestration.constants import Entity


class KernelPolicy(BasePolicy):
    @property
    def entity(self):
        return Entity.ANY, None


KernelPolicy.allow_actions(
    [
        constants.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

KernelPolicy.allow_actions(
    [
        constants.UPDATE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_notebook_edit_access(),
)

KernelPolicy.allow_read(
    KernelPresenter.default_attributes + [],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)


KernelPolicy.allow_read(
    KernelPresenter.default_attributes + [],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_notebook_edit_access(),
)

KernelPolicy.allow_write(
    [
        'action_type',
        'num_processes',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_notebook_edit_access(),
)
