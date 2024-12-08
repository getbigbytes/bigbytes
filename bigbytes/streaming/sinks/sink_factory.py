from typing import Dict

from bigbytes.data_preparation.decorators import collect_decorated_objs
from bigbytes.streaming.constants import GENERIC_IO_SINK_TYPES, SinkType


class SinkFactory:
    @classmethod
    def get_sink(self, config: Dict, **kwargs):
        connector_type = config['connector_type']
        if connector_type == SinkType.ACTIVEMQ:
            from bigbytes.streaming.sinks.activemq import ActiveMQSink

            return ActiveMQSink(config, **kwargs)
        elif connector_type == SinkType.AMAZON_S3:
            from bigbytes.streaming.sinks.amazon_s3 import AmazonS3Sink

            return AmazonS3Sink(config, **kwargs)
        elif connector_type == SinkType.AZURE_DATA_LAKE:
            from bigbytes.streaming.sinks.azure_data_lake import AzureDataLakeSink

            return AzureDataLakeSink(config, **kwargs)
        elif connector_type == SinkType.DUMMY:
            from bigbytes.streaming.sinks.dummy import DummySink

            return DummySink(config, **kwargs)
        elif connector_type == SinkType.ELASTICSEARCH:
            from bigbytes.streaming.sinks.elasticsearch import ElasticSearchSink

            return ElasticSearchSink(config, **kwargs)
        elif connector_type == SinkType.GOOGLE_CLOUD_PUBSUB:
            from bigbytes.streaming.sinks.google_cloud_pubsub import (
                GoogleCloudPubSubSink,
            )

            return GoogleCloudPubSubSink(config, **kwargs)
        elif connector_type == SinkType.GOOGLE_CLOUD_STORAGE:
            from bigbytes.streaming.sinks.google_cloud_storage import (
                GoogleCloudStorageSink,
            )

            return GoogleCloudStorageSink(config, **kwargs)
        elif connector_type == SinkType.INFLUXDB:
            from bigbytes.streaming.sinks.influxdb import InfluxDbSink

            return InfluxDbSink(config, **kwargs)
        elif connector_type == SinkType.KAFKA:
            from bigbytes.streaming.sinks.kafka import KafkaSink

            return KafkaSink(config, **kwargs)
        elif connector_type == SinkType.KINESIS:
            from bigbytes.streaming.sinks.kinesis import KinesisSink

            return KinesisSink(config, **kwargs)
        elif connector_type == SinkType.MONGODB:
            from bigbytes.streaming.sinks.mongodb import MongoDbSink

            return MongoDbSink(config, **kwargs)
        elif connector_type == SinkType.OPENSEARCH:
            from bigbytes.streaming.sinks.opensearch import OpenSearchSink

            return OpenSearchSink(config, **kwargs)
        elif connector_type == SinkType.ORACLEDB:
            from bigbytes.streaming.sinks.oracledb import OracleDbSink

            return OracleDbSink(config, **kwargs)
        elif connector_type == SinkType.POSTGRES:
            from bigbytes.streaming.sinks.postgres import PostgresSink

            return PostgresSink(config, **kwargs)
        elif connector_type == SinkType.RABBITMQ:
            from bigbytes.streaming.sinks.rabbitmq import RabbitMQSink

            return RabbitMQSink(config, **kwargs)
        elif connector_type in GENERIC_IO_SINK_TYPES:
            from bigbytes.streaming.sinks.generic_io import GenericIOSink

            return GenericIOSink(config, **kwargs)
        raise Exception(
            f'Ingesting data to {connector_type} is not supported in streaming pipelines yet.',
        )

    @classmethod
    def get_python_sink(self, content: str, **kwargs):
        """
        Find the class that's decorated with streaming_sink from the source code.

        Args:
            content (str): The python code that contains the streaming sink implementation.
            **kwargs: {'global_vars': {...}}

        Returns:
            The initialized class object.

        Raises:
            Exception: Description
        """
        decorated_sinks = []

        exec(content, {'streaming_sink': collect_decorated_objs(decorated_sinks)})

        if not decorated_sinks:
            raise Exception('Not find the class that has streaming_sink decorator.')

        return decorated_sinks[0](**kwargs)
