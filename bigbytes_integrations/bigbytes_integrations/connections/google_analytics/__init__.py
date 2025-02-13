from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from bigbytes_integrations.connections.base import Connection
from bigbytes_integrations.connections.google_analytics.constants import (
    DATE_STRING_PATTERN,
    DIMENSIONS,
    METRICS,
)
from bigbytes_integrations.connections.google_analytics.utils import parse_response
from bigbytes_integrations.connections.utils.google import CredentialsInfoType
from bigbytes_integrations.utils.dictionary import merge_dict
from typing import Literal
import os
import re


class GoogleAnalytics(Connection):
    def __init__(
        self,
        property_id: int,
        credentials_info: CredentialsInfoType = None,
        path_to_credentials_json_file: str = None,
    ):
        if not credentials_info and not path_to_credentials_json_file:
            raise Exception('GoogleAnalytics connection requires credentials_info '
                            'or path_to_credentials_json_file.')

        super().__init__()
        self.credentials_info = credentials_info
        self.path_to_credentials_json_file = path_to_credentials_json_file
        self.property_id = property_id

    def connect(self):
        """
        Create a connection to the Google Analytics API and return client object.
        """
        if self.credentials_info:
            client = BetaAnalyticsDataClient.from_service_account_info(self.credentials_info)
        elif self.path_to_credentials_json_file:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.path_to_credentials_json_file
            client = BetaAnalyticsDataClient()
        return client

    def get_metadata(self):
        client = self.connect()
        response = client.get_metadata(name=f'properties/{self.property_id}/metadata')
        return dict(
            dimensions=response.dimensions,
            metrics=response.metrics,
        )

    def load(
        self,
        start_date: str,
        end_date: str = 'today',
        dimensions: Literal[DIMENSIONS] = None,
        limit: int = None,
        metrics: Literal[METRICS] = None,
        offset: int = None,
    ):
        # if not re.match(DATE_STRING_PATTERN, start_date):
        #     raise Exception(f'start_date must match {DATE_STRING_PATTERN}')
        # if not re.match(DATE_STRING_PATTERN, end_date):
        #     raise Exception(f'end_date must match {DATE_STRING_PATTERN}')

        tags = self.build_tags(
            dimensions=dimensions,
            end_date=end_date,
            limit=limit,
            metrics=metrics,
            start_date=start_date,
        )

        client = self.connect()

        self.info('Loading started.', tags=tags)
        request = RunReportRequest(
            date_ranges=[DateRange(start_date=start_date, end_date='today')],
            dimensions=([Dimension(name=d) for d in dimensions] if dimensions else None),
            limit=limit,
            metrics=([Metric(name=d) for d in metrics] if metrics else None),
            property=f'properties/{self.property_id}',
            offset=offset,
        )

        data = []
        try:
            response = client.run_report(request)
            data = parse_response(request, response)
        except Exception as err:
            self.exception(f'Loading err: {err}.', tags=dict(
                error=err,
            ))

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''

        self.info('Loading completed.', tags=merge_dict(tags, dict(count=len(data))))

        return data
