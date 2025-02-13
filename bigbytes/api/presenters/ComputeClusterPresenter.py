from typing import Dict

from bigbytes.api.presenters.BasePresenter import BasePresenter
from bigbytes.shared.models import BaseDataClass


class ComputeClusterPresenter(BasePresenter):
    default_attributes = [
        'cluster',
    ]

    async def prepare_present(self, **kwargs) -> Dict:
        data = self.resource.model
        if 'cluster' in data:
            cluster = data.get('cluster')
            if isinstance(cluster, BaseDataClass):
                data['cluster'] = cluster.to_dict()

        return data
