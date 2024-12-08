from bigbytes.api.presenters.BasePresenter import BasePresenter


class ExtensionOptionPresenter(BasePresenter):
    default_attributes = [
        'description',
        'name',
        'templates',
        'uuid',
    ]
