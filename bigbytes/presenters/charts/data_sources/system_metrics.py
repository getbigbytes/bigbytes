import os

import pandas as pd

from bigbytes.data_preparation.models.constants import PIPELINES_FOLDER
from bigbytes.presenters.charts.data_sources.base import ChartDataSourceBase
from bigbytes.system.memory.presenters import to_dataframe


class ChartDataSourceSystemMetrics(ChartDataSourceBase):
    def load_data(
        self,
        **kwargs,
    ) -> pd.DataFrame:
        df = to_dataframe(
            os.path.join(
                PIPELINES_FOLDER,
                self.pipeline_uuid or '',
                self.block_uuid or '',
            ),
        ).to_pandas()
        return df
