from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.OutputPresenter import OutputPresenter
from bigbytes.data_preparation.repo_manager import get_project_uuid
from bigbytes.orchestration.constants import Entity
from bigbytes.orchestration.db.models.schedules import BlockRun


class OutputPolicy(BasePolicy):
    @property
    def entity(self):
        parent_model = self.options.get('parent_model')
        if parent_model:
            if type(parent_model) is BlockRun:
                return Entity.PIPELINE, parent_model.pipeline_run.pipeline_uuid

        return Entity.PROJECT, get_project_uuid()


OutputPolicy.allow_actions(
    [
        constants.CREATE,
        constants.DETAIL,
        constants.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

OutputPolicy.allow_read(
    OutputPresenter.default_attributes + [],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.CREATE,
        constants.DETAIL,
        constants.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

OutputPolicy.allow_write(
    [
        'block_uuid',
        'partition',
        'persist',
        'pipeline_uuid',
        'refresh',
        'sample_count',
        'streams',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.CREATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

OutputPolicy.allow_query(
    [
        'block_uuid',
        'parent_stream',
        'partition',
        'sample_count',
        'stream',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.DETAIL,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

OutputPolicy.allow_query(
    [
        'sample_count',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)
