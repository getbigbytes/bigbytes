from bigbytes.api.presenters.BasePresenter import BasePresenter


class BlockLayoutItemPresenter(BasePresenter):
    default_attributes = [
        "configuration",
        "content",
        "data",
        "data_source",
        "error",
        "name",
        "skip_render",
        "type",
        "uuid",
    ]
