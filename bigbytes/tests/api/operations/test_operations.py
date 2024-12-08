from unittest.mock import patch

from bigbytes.api.operations import constants
from bigbytes.data_preparation.models.constants import BlockType
from bigbytes.orchestration.db.models.oauth import User
from bigbytes.tests.api.operations.test_base import BaseApiTestCase


class OperationTests(BaseApiTestCase):
    @patch('bigbytes.settings.server.DISABLE_NOTEBOOK_EDIT_ACCESS', 1)
    @patch('bigbytes.api.utils.DISABLE_NOTEBOOK_EDIT_ACCESS', 1)
    @patch('bigbytes.api.policies.BasePolicy.DISABLE_NOTEBOOK_EDIT_ACCESS', 1)
    @patch('bigbytes.api.policies.BasePolicy.REQUIRE_USER_AUTHENTICATION', 0)
    async def test_execute_create_with_disable_edit_access(self):
        operation = self.build_operation(
            action=constants.CREATE,
            payload=dict(block=dict(
                name='test block',
                type=BlockType.DATA_LOADER,
            )),
            resource='blocks',
            user=None,
        )
        response = await operation.execute()

        self.assertIsNotNone(response['error'])

    @patch('bigbytes.settings.server.DISABLE_NOTEBOOK_EDIT_ACCESS', 1)
    @patch('bigbytes.api.utils.DISABLE_NOTEBOOK_EDIT_ACCESS', 1)
    @patch('bigbytes.api.policies.BasePolicy.DISABLE_NOTEBOOK_EDIT_ACCESS', 1)
    @patch('bigbytes.api.policies.BasePolicy.REQUIRE_USER_AUTHENTICATION', 1)
    async def test_execute_create_with_disable_edit_access_and_user(self):
        operation = self.build_operation(
            action=constants.CREATE,
            payload=dict(block=dict(
                name='test block',
                type=BlockType.DATA_LOADER,
            )),
            resource='blocks',
            user=User(),
        )
        response = await operation.execute()

        self.assertIsNotNone(response['error'])
