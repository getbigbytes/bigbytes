from bigbytes.shared.enum import StrEnum

ENV_DEV = 'dev'
ENV_PROD = 'prod'
ENV_STAGING = 'staging'
ENV_TEST = 'test'
ENV_TEST_BIGBYTES = 'test_bigbytes'

VALID_ENVS = frozenset([
    ENV_DEV,
    ENV_PROD,
    ENV_STAGING,
    ENV_TEST,
    ENV_TEST_BIGBYTES,
])

SAMPLE_SIZE = 1000

S3_PREFIX = 's3://'
GCS_PREFIX = 'gs://'

ENV_VAR_INSTANCE_TYPE = 'INSTANCE_TYPE'


class InstanceType(StrEnum):
    SERVER_AND_SCHEDULER = 'server_and_scheduler'
    SCHEDULER = 'scheduler'
    WEB_SERVER = 'web_server'
