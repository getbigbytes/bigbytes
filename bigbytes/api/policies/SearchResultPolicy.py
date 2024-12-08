from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.SearchResultPresenter import SearchResultPresenter


class SearchResultPolicy(BasePolicy):
    pass


SearchResultPolicy.allow_actions([
    constants.CREATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

SearchResultPolicy.allow_read(SearchResultPresenter.default_attributes, scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

SearchResultPolicy.allow_write([
    'pipeline_type',
    'query',
    'ratio',
    'type',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_viewer_role())
