from bigbytes.api.resources.DatabaseResource import DatabaseResource
from bigbytes.orchestration.db.models.oauth import Role, UserRole


class UserRoleResource(DatabaseResource):
    model_class = UserRole


UserRoleResource.register_parent_model('role_id', Role)
