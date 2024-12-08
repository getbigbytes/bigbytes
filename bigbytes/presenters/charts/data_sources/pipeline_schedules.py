from typing import Dict

import pandas as pd

from bigbytes.api.operations import constants
from bigbytes.api.operations.base import BaseOperation
from bigbytes.presenters.charts.data_sources.base import ChartDataSourceBase
from bigbytes.presenters.charts.data_sources.constants import DEFAULT_LIMIT
from bigbytes.shared.hash import merge_dict


class ChartDataSourcePipelineSchedules(ChartDataSourceBase):
    async def load_data(
        self,
        user=None,
        meta: Dict = None,
        variables: Dict = None,
        **kwargs,
    ):
        response = await BaseOperation(
            action=constants.LIST,
            meta=merge_dict({
                constants.META_KEY_LIMIT: DEFAULT_LIMIT,
            }, meta or {}),
            query=variables,
            resource='pipeline_schedules',
            resource_parent='pipelines' if self.pipeline_uuid else None,
            resource_parent_id=self.pipeline_uuid if self.pipeline_uuid else None,
            user=user,
        ).execute()

        return pd.DataFrame(response['pipeline_schedules'])
