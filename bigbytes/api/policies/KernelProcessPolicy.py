from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.KernelProcessPresenter import KernelProcessPresenter
from bigbytes.orchestration.constants import Entity


class KernelProcessPolicy(BasePolicy):
    @property
    def entity(self):
        # Adjust the entity to reflect the KernelProcess's entity, if applicable
        return Entity.ANY, None


KernelProcessPolicy.allow_actions(
    [
        constants.DETAIL,
        constants.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

KernelProcessPolicy.allow_actions(
    [
        constants.DELETE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_notebook_edit_access(),
)


KernelProcessPolicy.allow_read(
    KernelProcessPresenter.default_attributes,
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.DETAIL,
        constants.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

KernelProcessPolicy.allow_query(
    ['check_active_status'],
    on_action=[
        constants.DETAIL,
        constants.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)
