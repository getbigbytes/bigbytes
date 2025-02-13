from bigbytes.api.presenters.BasePresenter import BasePresenter
import os


class FolderPresenter(BasePresenter):
    default_attributes = [
        'name',
        'path',
    ]

    def name(self, **kwargs) -> str:
        return os.path.basename(self.resource.path)
