from typing import Dict

from bigbytes.api.presenters.BasePresenter import BasePresenter


class ComputeServicePresenter(BasePresenter):
    default_attributes = [
        'connection_credentials',
        'clusters',
        'setup_steps',
        'uuid',
    ]

    async def prepare_present(self, **kwargs) -> Dict:
        return self.resource.model.to_dict()
