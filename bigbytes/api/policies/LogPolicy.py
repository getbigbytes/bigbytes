from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.LogPresenter import LogPresenter
from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.data_preparation.repo_manager import get_project_uuid
from bigbytes.orchestration.constants import Entity
from bigbytes.orchestration.db.models.schedules import BlockRun


class LogPolicy(BasePolicy):
    @property
    def entity(self):
        parent_model = self.options.get('parent_model')
        if parent_model:
            if type(parent_model) is BlockRun:
                return Entity.PIPELINE, parent_model.pipeline_run.pipeline_uuid
            elif issubclass(parent_model.__class__, Pipeline):
                return Entity.PIPELINE, parent_model.uuid

        return Entity.PROJECT, get_project_uuid()


LogPolicy.allow_actions([
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

LogPolicy.allow_read(LogPresenter.default_attributes + [
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())

LogPolicy.allow_query([
    'block_run_id',
    'block_run_id[]',
    'block_type',
    'block_type[]',
    'block_uuid',
    'block_uuid[]',
    'end_timestamp',
    'level[]',
    'pipeline_run_id',
    'pipeline_run_id[]',
    'pipeline_schedule_id',
    'pipeline_schedule_id[]',
    'start_timestamp',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())
