from bigbytes.api.presenters.BasePresenter import BasePresenter
from bigbytes.api.presenters.mixins.users import AssociatedUserPresenter


class SessionPresenter(BasePresenter, AssociatedUserPresenter):
    default_attributes = [
        'expires',
        'token',
        'user',
    ]
