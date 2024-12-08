from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.FileContentPresenter import FileContentPresenter


class FileContentPolicy(BasePolicy):
    pass


FileContentPolicy.allow_actions([
    constants.DETAIL,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

FileContentPolicy.allow_actions([
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access())

FileContentPolicy.allow_read(FileContentPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.DETAIL,
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

FileContentPolicy.allow_write([
    'block_uuid',
    'content',
    'modified_timestamp',
    'name',
    'path',
    'pipeline_uuid',
    'size',
    'version',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access())
