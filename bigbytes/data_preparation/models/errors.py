from bigbytes.errors.base import BigbytesBaseException


class FileExistsError(BigbytesBaseException):
    pass


class FileNotInProjectError(BigbytesBaseException):
    pass


class FileWriteError(BigbytesBaseException):
    pass


class SerializationError(BigbytesBaseException):
    pass


class PipelineZipTooLargeError(BigbytesBaseException):
    pass


class InvalidPipelineZipError(BigbytesBaseException):
    pass
