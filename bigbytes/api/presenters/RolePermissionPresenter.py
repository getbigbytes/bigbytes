from bigbytes.api.presenters.BasePresenter import BasePresenter


class RolePermissionPresenter(BasePresenter):
    default_attributes = [
        'created_at',
        'id',
        'permission_id',
        'role_id',
        'updated_at',
    ]
