import json

from bigbytes.api.errors import ApiError
from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.data_preparation.models.triggers import ScheduleType
from bigbytes.orchestration.db import safe_db_query
from bigbytes.orchestration.db.models.schedules import PipelineRun, PipelineSchedule
from bigbytes.orchestration.triggers.utils import create_and_start_pipeline_run
from bigbytes.server.api.base import BaseHandler
from bigbytes.server.api.errors import UnauthenticatedRequestException
from bigbytes.shared.requests import get_bearer_auth_token_from_headers


class ApiTriggerPipelineHandler(BaseHandler):
    model_class = PipelineRun

    @safe_db_query
    def post(self, pipeline_schedule_id, token: str = None):
        pipeline_schedule = PipelineSchedule.query.get(int(pipeline_schedule_id))
        if not pipeline_schedule:
            raise ApiError(ApiError.RESOURCE_NOT_FOUND)

        if token is None:
            token = get_bearer_auth_token_from_headers(self.request.headers)

        if ScheduleType.API == pipeline_schedule.schedule_type and \
            pipeline_schedule.token and \
                pipeline_schedule.token != token:
            raise UnauthenticatedRequestException(
                f'Invalid token for pipeline schedule ID {pipeline_schedule_id}.',
            )

        payload = self.get_payload()
        if 'variables' not in payload:
            payload['variables'] = {}

        body = self.request.body
        if body:
            payload['event_variables'] = {}

            for k, v in json.loads(body).items():
                if k == 'pipeline_run':
                    continue
                payload['event_variables'][k] = v

        pipeline = Pipeline.get(
            pipeline_schedule.pipeline_uuid, repo_path=pipeline_schedule.repo_path
        )
        pipeline_run = create_and_start_pipeline_run(
            pipeline,
            pipeline_schedule,
            payload,
            should_schedule=False,
        )

        self.write(dict(pipeline_run=pipeline_run.to_dict()))
