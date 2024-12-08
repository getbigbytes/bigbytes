from dataclasses import dataclass
from bigbytes.shared.config import BaseConfig


@dataclass
class DbtConfig(BaseConfig):
    account_id: int
    api_token: str
