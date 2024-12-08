import os
from unittest.mock import patch

from bigbytes.data_preparation.git import Git
from bigbytes.tests.api.endpoints.mixins import BaseAPIEndpointTest
from bigbytes.tests.shared.mixins import ProjectPlatformMixin


class GitTest(BaseAPIEndpointTest):
    def test_repo_path(self):
        self.assertEqual(Git().repo_path, os.getcwd())


class GitProjectPlatformTest(ProjectPlatformMixin):
    def test_repo_path(self):
        git_settings = dict(
            path='bigbytes_custom_path',
        )
        with patch('bigbytes.data_preparation.git.project_platform_activated', lambda: True):
            with patch(
                'bigbytes.data_preparation.git.git_settings',
                lambda user=None, **kwargs: git_settings,
            ):
                self.assertEqual(Git().repo_path, 'bigbytes_custom_path')
