from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.PipelineExecutionFrameworkPresenter import (
    PipelineExecutionFrameworkPresenter,
)
from bigbytes.orchestration.constants import Entity


class PipelineExecutionFrameworkPolicy(BasePolicy):
    @property
    def entity(self):
        # Adjust the entity to reflect the KernelProcess's entity, if applicable
        return Entity.ANY, None


PipelineExecutionFrameworkPolicy.allow_actions(
    [
        OperationType.DETAIL,
        OperationType.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

PipelineExecutionFrameworkPolicy.allow_actions(
    [
        OperationType.CREATE,
        OperationType.DELETE,
        OperationType.UPDATE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)


PipelineExecutionFrameworkPolicy.allow_read(
    PipelineExecutionFrameworkPresenter.default_attributes,
    on_action=[
        OperationType.DETAIL,
        OperationType.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

PipelineExecutionFrameworkPolicy.allow_read(
    PipelineExecutionFrameworkPresenter.default_attributes,
    on_action=[
        OperationType.CREATE,
        OperationType.DELETE,
        OperationType.UPDATE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)

PipelineExecutionFrameworkPolicy.allow_write(
    [
        'clone_pipeline_uuid',
        'custom_template_uuid',
        'description',
        'name',
        'tags',
        'type',
        'uuid',
    ],
    on_action=[
        OperationType.CREATE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)

PipelineExecutionFrameworkPolicy.allow_write(
    [
        'blocks',
        'description',
        'name',
        'pipelines',
        'settings',
        'tags',
        'type',
    ],
    on_action=[
        OperationType.UPDATE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)
