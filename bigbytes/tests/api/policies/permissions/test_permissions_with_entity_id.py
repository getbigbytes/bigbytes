from unittest.mock import patch

from bigbytes.tests.api.mixins import BootstrapMixin
from bigbytes.tests.api.operations.test_base import BaseApiTestCase
from bigbytes.tests.api.policies.permissions.mixins import PermissionsMixin


@patch('bigbytes.api.policies.BasePolicy.REQUIRE_USER_AUTHENTICATION', 1)
@patch('bigbytes.api.policies.BasePolicy.REQUIRE_USER_PERMISSIONS', 1)
class PermissionsWithEntityIDTest(BaseApiTestCase, BootstrapMixin, PermissionsMixin):
    def test_authorized(self):
        pass

    def test_unauthorized(self):
        pass
