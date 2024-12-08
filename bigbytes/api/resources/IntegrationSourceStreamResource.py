from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.data_preparation.models.pipelines.integration_pipeline import (
    IntegrationPipeline,
)
from bigbytes.orchestration.db import safe_db_query
from bigbytes.settings.repo import get_repo_path


class IntegrationSourceStreamResource(GenericResource):
    @classmethod
    @safe_db_query
    def member(self, pk, user, **kwargs):
        repo_path = get_repo_path(user=user)
        return self(IntegrationPipeline.get(pk, repo_path=repo_path), user, **kwargs)
