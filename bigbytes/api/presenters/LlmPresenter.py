from bigbytes.api.presenters.BasePresenter import BasePresenter


class LlmPresenter(BasePresenter):
    default_attributes = [
        'use_case',
        'response',
    ]
