from bigbytes.api.presenters.BasePresenter import BasePresenter


class OauthPresenter(BasePresenter):
    default_attributes = [
        'authenticated',
        'expires',
        'provider',
        'url',
        'redirect_query_params',
    ]
