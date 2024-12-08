from bigbytes.errors.base import BigbytesBaseException
from typing import Dict


class DoesNotExistError(BigbytesBaseException):
    pass


class ValidationError(BigbytesBaseException):
    def __init__(self, error: str, metadata: Dict):
        self.error = error
        self.metadata = metadata

    def to_dict(self):
        return dict(
            error=self.error,
            metadata=self.metadata,
        )
