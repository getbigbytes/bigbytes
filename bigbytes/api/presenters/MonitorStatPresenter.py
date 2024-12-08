from bigbytes.api.presenters.BasePresenter import BasePresenter


class MonitorStatPresenter(BasePresenter):
    default_attributes = [
        'stats_type',
        'stats',
    ]
