from bigbytes.api.presenters.BasePresenter import BasePresenter


class DataProviderPresenter(BasePresenter):
    default_attributes = [
        'id',
        'profiles',
        'value',
    ]
