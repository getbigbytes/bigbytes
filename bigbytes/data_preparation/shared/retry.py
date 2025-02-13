from dataclasses import dataclass

from bigbytes.shared.config import BaseConfig


@dataclass
class RetryConfig(BaseConfig):
    retries: int = 0
    delay: int = 5
    max_delay: int = 60
    exponential_backoff: bool = True
