import os

from bigbytes.settings.utils import base_repo_dirname, base_repo_name, base_repo_path
from bigbytes.tests.shared.mixins import ProjectPlatformMixin


class SettingsUtilsTest(ProjectPlatformMixin):
    def test_base_repo_dirname(self):
        self.assertEqual(base_repo_dirname(), os.path.dirname(base_repo_path()))

    def test_base_repo_name(self):
        self.assertEqual(base_repo_name(), 'test')

    def test_base_repo_path(self):
        self.assertEqual(base_repo_path(), base_repo_path())
