from bigbytes.api.operations import constants
from bigbytes.api.presenters.BasePresenter import BasePresenter


class IntegrationDestinationPresenter(BasePresenter):
    default_attributes = [
        'name',
        'templates',
        'uuid',
    ]


IntegrationDestinationPresenter.register_format(
    constants.CREATE,
    [
        'error_message',
        'success',
    ],
)
