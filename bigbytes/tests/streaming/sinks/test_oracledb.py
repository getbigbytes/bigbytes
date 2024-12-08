from unittest.mock import patch

from bigbytes.streaming.sinks.oracledb import OracleDbSink
from bigbytes.tests.base_test import TestCase


class OracleDbTests(TestCase):
    def test_init(self):
        with patch.object(OracleDbSink, 'init_client') as mock_init_client:
            OracleDbSink(dict(
                connector_type='oracledb',
                user='test',
                password='123456',
                host='oracle-test',
                port=1521,
                table='test_table',
                service_name='test_service',
                mode='thin',
            ))
            mock_init_client.assert_called_once()

    def test_init_invalid_config(self):
        with patch.object(OracleDbSink, 'init_client') as mock_init_client:
            with self.assertRaises(Exception) as context:
                OracleDbSink(dict(
                    connector_type='oracledb',
                    user='test',
                    password='123456',
                    host='oracle-test',
                    port=1521,
                    table='test_table',
                    mode='thin',
                ))
            self.assertTrue(
                '__init__() missing 1 required positional argument: \'service_name\''
                in str(context.exception),
            )
            self.assertEqual(mock_init_client.call_count, 0)
