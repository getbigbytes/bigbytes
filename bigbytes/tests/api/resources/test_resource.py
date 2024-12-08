import secrets

from bigbytes.api.resources.Resource import Resource
from bigbytes.tests.base_test import DBTestCase


class ResourceTest(DBTestCase):
    def test_instantiation(self):
        options = dict(fire=1, water=2)
        model = secrets.token_urlsafe()
        current_user = secrets.token_urlsafe()
        result_set_from_external = secrets.token_urlsafe()

        resource = Resource(
            model,
            current_user,
            result_set_from_external=result_set_from_external,
            **options
        )

        self.assertEqual(resource.model, model)
        self.assertEqual(resource.current_user, current_user)
        self.assertEqual(resource.result_set_from_external, result_set_from_external)
        self.assertEqual(resource.model_options, options)
        self.assertIsNone(resource.result_set_attr)
