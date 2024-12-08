import os
from unittest.mock import call, patch

import yaml

from bigbytes.data_preparation.models.project import Project
from bigbytes.data_preparation.models.project.constants import FeatureUUID
from bigbytes.server.constants import VERSION
from bigbytes.settings.platform import platform_settings_full_path
from bigbytes.settings.repo import get_repo_path
from bigbytes.settings.utils import base_repo_path
from bigbytes.shared.io import safe_write
from bigbytes.tests.base_test import AsyncDBTestCase
from bigbytes.tests.settings.test_platform import SETTINGS
from bigbytes.tests.shared.mixins import ProjectPlatformMixin


class ProjectTest(ProjectPlatformMixin, AsyncDBTestCase):
    def test_init(self):
        with patch(
            'bigbytes.data_preparation.models.project.project_platform_activated',
            lambda: False,
        ):
            with patch(
                'bigbytes.data_preparation.models.project.get_repo_config',
            ) as mock_get_repo_config:
                project = Project(repo_path=base_repo_path())

                self.assertEqual(project.name, 'test')
                self.assertEqual(project.repo_path, base_repo_path())
                self.assertEqual(project.settings, None)
                self.assertEqual(project.version, VERSION)
                self.assertFalse(project.root_project)

                mock_get_repo_config.assert_not_called()
                project.repo_config
                mock_get_repo_config.assert_called_once_with(
                    repo_path=base_repo_path(),
                    root_project=False,
                )

        project = Project(repo_path=os.path.join(base_repo_path(), 'bigbytes_platform'))
        self.assertEqual(project.name, 'bigbytes_platform')
        self.assertEqual(project.repo_path, os.path.join(base_repo_path(), 'bigbytes_platform'))

        with patch(
            'bigbytes.data_preparation.models.project.get_repo_config',
        ) as mock_get_repo_config:
            project = Project(root_project=True)
            self.assertEqual(project.name, 'test')
            self.assertEqual(project.repo_path, base_repo_path())
            self.assertEqual(project.settings, None)
            self.assertEqual(project.version, VERSION)
            self.assertTrue(project.root_project)

            # mock_get_repo_config.assert_not_called()
            project.repo_config
            # mock_get_repo_config.assert_called_once_with(
            #     repo_path=base_repo_path(),
            #     root_project=True,
            # )

    def test_init_project_platform(self):
        with patch('bigbytes.settings.platform.project_platform_activated', lambda: True):
            with patch(
                'bigbytes.data_preparation.models.project.project_platform_activated',
                lambda: True,
            ):
                with patch('bigbytes.settings.repo.project_platform_activated', lambda: True):
                    with patch(
                        'bigbytes.data_preparation.models.project.get_repo_config',
                    ) as mock_get_repo_config:
                        project = Project(root_project=False)

                        self.assertEqual(project.name, 'bigbytes_platform')
                        self.assertEqual(
                            project.repo_path, os.path.join(base_repo_path(), 'bigbytes_platform'),
                        )
                        self.assertEqual(project.settings, dict(
                            active=True,
                            uuid='bigbytes_platform',
                        ))
                        self.assertEqual(project.version, VERSION)
                        self.assertFalse(project.root_project)

                        project.repo_config
                        self.assertEqual(
                            mock_get_repo_config.mock_calls[0],
                            call(
                                repo_path=base_repo_path(),
                                root_project=True,
                            ),
                        )
                        self.assertEqual(
                            mock_get_repo_config.mock_calls[1],
                            call(
                                repo_path=os.path.join(base_repo_path(), 'bigbytes_platform'),
                                root_project=False,
                            ),
                        )

                    with patch(
                        'bigbytes.data_preparation.models.project.get_repo_config',
                    ) as mock_get_repo_config:
                        project = Project(root_project=True)

                        self.assertEqual(project.name, 'test')
                        self.assertEqual(project.repo_path, base_repo_path())
                        self.assertEqual(project.settings, None)
                        self.assertEqual(project.version, VERSION)
                        self.assertTrue(project.root_project)

                        project.repo_config
                        self.assertEqual(
                            mock_get_repo_config.mock_calls[0],
                            call(
                                repo_path=base_repo_path(),
                                root_project=True,
                            ),
                        )
                        self.assertEqual(
                            mock_get_repo_config.mock_calls[1],
                            call(
                                repo_path=base_repo_path(),
                                root_project=True,
                            ),
                        )

    def test_repo_path_for_database_query(self):
        content = yaml.dump(SETTINGS)
        safe_write(platform_settings_full_path(), content)

        with patch('bigbytes.settings.platform.project_platform_activated', lambda: True):
            with patch(
                'bigbytes.data_preparation.models.project.project_platform_activated',
                lambda: True,
            ):
                project = Project(root_project=False)

                self.assertEqual(
                    sorted(project.repo_path_for_database_query('pipeline_schedules')),
                    sorted([
                        get_repo_path(root_project=False),
                        os.path.join(os.path.dirname(base_repo_path()), 'default_repo'),
                        os.path.join(
                            os.path.dirname(base_repo_path()),
                            'default_repo/default_repo',
                        ),
                    ]),
                )

                self.assertEqual(
                    sorted(project.repo_path_for_database_query('secrets')),
                    sorted([
                        get_repo_path(root_project=False),
                        os.path.join(os.path.dirname(base_repo_path()), 'default_repo2'),
                        os.path.join(
                            os.path.dirname(base_repo_path()),
                            'default_repo2/default_repo',
                        ),
                    ]),
                )

                project = Project(root_project=True)

                self.assertEqual(project.repo_path_for_database_query('pipeline_schedules'), [
                    base_repo_path(),
                ])

                self.assertEqual(project.repo_path_for_database_query('secrets'), [
                    base_repo_path(),
                ])

    def test_projects(self):
        with patch(
            'bigbytes.data_preparation.models.project.project_platform_settings',
        ) as mock_project_platform_settings:
            Project().projects()
            mock_project_platform_settings.assert_called_with(
                context_data=dict(),
                bigbytes_projects_only=True,
            )

    def test_is_feature_enabled(self):
        project = Project()
        features = {
            FeatureUUID.GLOBAL_HOOKS: True,
        }

        with patch.object(project.repo_config, 'features', features):
            self.assertFalse(project.is_feature_enabled(FeatureUUID.COMPUTE_MANAGEMENT))
            self.assertTrue(project.is_feature_enabled(FeatureUUID.GLOBAL_HOOKS))
