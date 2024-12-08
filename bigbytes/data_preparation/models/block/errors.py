from bigbytes.errors.base import BigbytesBaseException


class NoMultipleDynamicUpstreamBlocks(BigbytesBaseException):
    pass


class HasDownstreamDependencies(BigbytesBaseException):
    pass
