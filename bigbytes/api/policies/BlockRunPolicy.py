from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.BlockRunPresenter import BlockRunPresenter
from bigbytes.orchestration.constants import Entity


class BlockRunPolicy(BasePolicy):
    @property
    def entity(self):
        query = self.options.get('query', {})
        pipeline_uuid = query.get('pipeline_uuid', [None])
        if pipeline_uuid:
            pipeline_uuid = pipeline_uuid[0]
        if pipeline_uuid:
            return Entity.PIPELINE, pipeline_uuid

        parent_model = self.options.get('parent_model')
        if parent_model:
            return Entity.PIPELINE, parent_model.pipeline_uuid

        return super().entity


BlockRunPolicy.allow_actions([
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

BlockRunPolicy.allow_read(BlockRunPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())

BlockRunPolicy.allow_query([
    'order_by',
    'pipeline_run_id',
    'pipeline_uuid',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())
