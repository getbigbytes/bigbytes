import os
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

import yaml
from croniter import croniter

from bigbytes.data_preparation.models.constants import PIPELINES_FOLDER
from bigbytes.settings.repo import get_repo_path
from bigbytes.shared.config import BaseConfig
from bigbytes.shared.constants import VALID_ENVS
from bigbytes.shared.enum import StrEnum
from bigbytes.shared.hash import index_by
from bigbytes.shared.io import safe_write
from bigbytes.shared.yaml import load_yaml

TRIGGER_FILE_NAME = 'triggers.yaml'


class ScheduleStatus(StrEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class ScheduleType(StrEnum):
    API = 'api'
    EVENT = 'event'
    TIME = 'time'


SCHEDULE_TYPE_TO_LABEL = {
    ScheduleType.API: 'API',
    ScheduleType.EVENT: 'Event',
    ScheduleType.TIME: 'Schedule',
}


class ScheduleInterval(StrEnum):
    ONCE = '@once'
    HOURLY = '@hourly'
    DAILY = '@daily'
    WEEKLY = '@weekly'
    MONTHLY = '@monthly'
    ALWAYS_ON = '@always_on'


@dataclass
class SettingsConfig(BaseConfig):
    skip_if_previous_running: bool = False
    allow_blocks_to_fail: bool = False
    create_initial_pipeline_run: bool = False
    landing_time_enabled: bool = False
    pipeline_run_limit: int = None
    timeout: int = None  # in seconds
    timeout_status: str = None


@dataclass
class Trigger(BaseConfig):
    name: str
    pipeline_uuid: str
    schedule_type: ScheduleType
    start_time: datetime
    schedule_interval: str
    status: ScheduleStatus = ScheduleStatus.INACTIVE
    last_enabled_at: datetime = None
    variables: Dict = field(default_factory=dict)
    sla: int = None  # in seconds
    settings: Dict = field(default_factory=dict)
    envs: List = field(default_factory=list)
    repo_path: str = None
    description: Optional[str] = None
    token: Optional[str] = None

    def __post_init__(self):
        if self.schedule_type and type(self.schedule_type) is str:
            self.schedule_type = ScheduleType(self.schedule_type)
        if self.status and type(self.status) is str:
            self.status = ScheduleStatus(self.status)
        if any(env not in VALID_ENVS for env in self.envs):
            raise Exception(
                f'Please provide valid env values inside {list(VALID_ENVS)}.'
            )

    @property
    def has_valid_schedule_interval(self) -> bool:
        # Check if trigger has valid cron expression
        if (
            self.schedule_interval is not None
            and self.schedule_type == ScheduleType.TIME
            and self.schedule_interval not in [e.value for e in ScheduleInterval]
            and not croniter.is_valid(self.schedule_interval)
        ):
            return False

        return True

    def to_dict(self) -> Dict:
        return dict(
            envs=self.envs,
            last_enabled_at=self.last_enabled_at,
            name=self.name,
            pipeline_uuid=self.pipeline_uuid,
            schedule_interval=self.schedule_interval,
            schedule_type=self.schedule_type.value
            if self.schedule_type
            else self.schedule_type,
            settings=self.settings,
            sla=self.sla,
            description=self.description,
            token=self.token,
            start_time=self.start_time,
            status=self.status.value if self.status else self.status,
            variables=self.variables,
        )


"""
Cache the triggers config by pipeline uuid
  Key: trigger_file_path
  Value: {"updated_at": xxx, "triggers": []}
"""
triggers_cache = dict()


def get_triggers_file_path(
    pipeline_uuid: str,
    repo_path: str = None
) -> str:
    pipeline_path = os.path.join(repo_path or get_repo_path(), PIPELINES_FOLDER, pipeline_uuid)
    trigger_file_path = os.path.join(pipeline_path, TRIGGER_FILE_NAME)
    return trigger_file_path


def load_triggers_file_content(
    pipeline_uuid: str,
    repo_path: str = None,
) -> str:
    content = None

    trigger_file_path = get_triggers_file_path(pipeline_uuid, repo_path=repo_path)
    if os.path.exists(trigger_file_path):
        with open(trigger_file_path) as fp:
            content = fp.read()

    return content


def load_triggers_file_data(pipeline_uuid: str) -> Dict:
    data = {}

    content = load_triggers_file_content(pipeline_uuid)
    if content:
        data = yaml.safe_load(content) or {}

    return data


def get_triggers_by_pipeline_with_cache(
    pipeline_uuid: str,
    repo_path: str = None,
):
    """
    Retrieve triggers for a given pipeline, utilizing a cache to avoid unnecessary file reads.

    This function checks if the trigger file for the specified pipeline has been modified since
    the last time it was cached. If the file has not been modified, the cached triggers are
    returned. If the file has been modified or is not in the cache, it reads the file, updates
    the cache, and returns the triggers.

    Args:
        pipeline_uuid (str): The unique identifier of the pipeline.
        repo_path (str, optional): The path to the repository containing the pipeline. Defaults to
            None.

    Returns:
        tuple: A tuple containing:
            - triggers (list): A list of triggers for the specified pipeline.
            - from_cache (bool): A boolean indicating whether the triggers were retrieved from the
                cache.

    Raises:
        Exception: If there is an error loading the triggers file or parsing the triggers
            configuration.
    """
    trigger_file_path = get_triggers_file_path(
        pipeline_uuid,
        repo_path=repo_path,
    )

    if not os.path.exists(trigger_file_path):
        return [], False

    trigger_file_updated_at = datetime.fromtimestamp(
        os.path.getmtime(trigger_file_path),
        tz=timezone.utc,
    )

    if trigger_file_path in triggers_cache:
        # Try reading triggers from cache first
        triggers_config = triggers_cache[trigger_file_path]
        last_updated_at = triggers_config.get('updated_at')
        triggers = triggers_config.get('triggers')
        if last_updated_at and triggers and last_updated_at >= trigger_file_updated_at:
            # Trigger file not modified since last time
            return triggers, True

    try:
        content = load_triggers_file_content(
            pipeline_uuid,
            repo_path=repo_path,
        )
        triggers = load_trigger_configs(
            content,
            pipeline_uuid=pipeline_uuid,
            repo_path=repo_path,
        )
        # Update the cache with the new triggers and their update time
        triggers_cache[trigger_file_path] = {
            'updated_at': trigger_file_updated_at,
            'triggers': triggers,
        }
    except Exception:
        traceback.print_exc()
        triggers = []

    return triggers, False


def get_triggers_by_pipeline(
    pipeline_uuid: str,
    repo_path: str = None,
) -> List[Trigger]:
    # For backward compatibility
    triggers, _ = get_triggers_by_pipeline_with_cache(pipeline_uuid, repo_path=repo_path)
    return triggers


def get_trigger_configs_by_name(pipeline_uuid: str) -> Dict:
    yaml_config = load_triggers_file_data(pipeline_uuid)
    trigger_configs = yaml_config.get('triggers') or {}
    trigger_configs_by_name = index_by(
        lambda config: config.get('name'),
        trigger_configs,
    )

    return trigger_configs_by_name


def build_triggers(
    trigger_configs: Dict,
    pipeline_uuid: str = None,
    raise_exception: bool = False,
    repo_path: str = None,
) -> List[Trigger]:
    triggers = []
    for trigger_config in trigger_configs:
        if pipeline_uuid:
            trigger_config['pipeline_uuid'] = pipeline_uuid
        try:
            trigger = Trigger.load(config=trigger_config)
            if trigger.repo_path is None:
                trigger.repo_path = repo_path

            # Add flag to settings so frontend can detect triggers with invalid cron expressions
            if not trigger.has_valid_schedule_interval:
                if not trigger.settings:
                    trigger.settings = dict()
                trigger.settings['invalid_schedule_interval'] = True

            triggers.append(trigger)
        except Exception as e:
            if raise_exception:
                raise Exception(
                    f'Failed to parse trigger config {trigger_config}. {str(e)}'
                ) from e
            else:
                print(f'Failed to parse trigger config for pipeline {pipeline_uuid}')
                traceback.print_exc()
    return triggers


def load_trigger_configs(
    content: str,
    pipeline_uuid: str = None,
    repo_path: str = None,
    raise_exception: bool = False,
    user=None,
) -> List[Trigger]:
    yaml_config = load_yaml(content) or {}
    trigger_configs = yaml_config.get('triggers') or {}

    return build_triggers(
        trigger_configs,
        pipeline_uuid,
        raise_exception,
        repo_path=repo_path or get_repo_path(),
    )


def add_or_update_trigger_for_pipeline_and_persist(
    trigger: Trigger,
    pipeline_uuid: str,
    update_only_if_exists: bool = False,
    old_trigger_name: str = None,
) -> Dict:
    trigger_configs_by_name = get_trigger_configs_by_name(pipeline_uuid)

    """
    The Trigger class has an "envs" attribute that the PipelineSchedule class does not
    have, so we need to set "envs" on the updated trigger if it already exists.
    Otherwise, it will get overwritten when updating the trigger in code.
    """
    trigger_name = trigger.name if old_trigger_name is None else old_trigger_name
    existing_trigger = trigger_configs_by_name.get(trigger_name)
    if existing_trigger is not None:
        trigger.envs = existing_trigger.get('envs', [])
    elif update_only_if_exists:
        return None

    trigger_configs_by_name[trigger_name] = trigger.to_dict()
    yaml_config = dict(triggers=list(trigger_configs_by_name.values()))
    content = yaml.safe_dump(yaml_config)
    trigger_file_path = get_triggers_file_path(pipeline_uuid)
    safe_write(trigger_file_path, content)

    return trigger_configs_by_name


def update_triggers_for_pipeline_and_persist(
    trigger_configs: List[Dict],
    pipeline_uuid: str,
) -> Dict:
    """
    Used to update all of a pipeline's triggers saved in code at once.
    Overwrites triggers in triggers.yaml config with updated triggers
    passed as first argument.
    """
    yaml_config = dict(triggers=trigger_configs)
    content = yaml.safe_dump(yaml_config)
    trigger_file_path = get_triggers_file_path(pipeline_uuid)
    safe_write(trigger_file_path, content)

    return trigger_configs


def remove_trigger(
    name: str,
    pipeline_uuid: str,
) -> Dict:
    trigger_configs_by_name = get_trigger_configs_by_name(pipeline_uuid)
    deleted_trigger = trigger_configs_by_name.pop(name, None)
    if deleted_trigger is not None:
        update_triggers_for_pipeline_and_persist(
            list(trigger_configs_by_name.values()),
            pipeline_uuid,
        )

    return deleted_trigger
