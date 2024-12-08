from dataclasses import dataclass
from bigbytes.shared.config import BaseConfig


@dataclass
class HightouchConfig(BaseConfig):
    api_key: str
