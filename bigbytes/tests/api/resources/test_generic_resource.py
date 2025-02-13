import secrets

from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.tests.api.operations.test_base import BaseApiTestCase


class GenericResourceTest(BaseApiTestCase):
    def test_missing(self):
        power = secrets.token_urlsafe()
        resource = GenericResource(dict(power=power), None)

        self.assertEqual(resource.power, power)
