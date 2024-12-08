from dataclasses import dataclass, field
from typing import Dict

from bigbytes.shared.config import BaseConfig
from bigbytes.shared.enum import StrEnum
from bigbytes.shared.logger import LoggingLevel


class LoggerType(StrEnum):
    DEFAULT = 'file'
    S3 = 's3'
    GCS = 'gcs'


@dataclass
class LoggingConfig(BaseConfig):
    type: LoggerType = LoggerType.DEFAULT
    level: LoggingLevel = LoggingLevel.INFO
    destination_config: Dict = field(default_factory=dict)
    # The period to keep the log files, e.g. '30d', '24h', '3w'
    retention_period: str = None
