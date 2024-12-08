from dataclasses import dataclass

from bigbytes.shared.config import BaseConfig


@dataclass
class ContainerInstanceConfig(BaseConfig):
    cpu: int = 1        # Number of CPU cores
    memory: int = 1     # Memory in GB
