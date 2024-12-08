import os
from unittest.mock import patch

import yaml
from jinja2 import Template

from bigbytes.data_preparation.shared.utils import get_template_vars_no_db
from bigbytes.settings.platform import (
    activate_project,
    active_project_settings,
    build_active_project_repo_path,
    build_repo_path_for_all_projects,
    get_repo_paths_for_file_path,
    git_settings,
    local_platform_settings_full_path,
    platform_settings,
    platform_settings_full_path,
    project_platform_activated,
    project_platform_settings,
    repo_path_from_database_query_to_project_repo_path,
)
from bigbytes.settings.platform.constants import set_project_platform_activated_flag
from bigbytes.settings.utils import base_repo_path
from bigbytes.tests.shared.mixins import ProjectPlatformMixin

SETTINGS = dict(
    projects=dict(
        bigbytes_platform=dict(
            database=dict(
                query=dict(
                    pipeline_schedules=[
                        'default_repo',
                        'default_repo/default_repo',
                    ],
                    secrets=[
                        'default_repo2',
                        'default_repo2/default_repo',
                    ],
                ),
            ),
            git=dict(
                path='bigbytes_platform/git',
            ),
        ),
        bigbytes_data=dict(
            git=dict(
                path='bigbytes_data/dev',
            ),
            path='bigbytes_data/platform',
        ),
    ),
)


@patch(
    'bigbytes.data_preparation.models.block.platform.utils.project_platform_activated',
    lambda: True,
)
@patch('bigbytes.settings.platform.project_platform_activated', lambda: True)
class PlatformSettingsTest(ProjectPlatformMixin):
    def setUp(self):
        super().setUp()
        # Write platform settings to settings.yaml file and set bigbytes_platform to active
        self.initialize_settings(SETTINGS)
        self.__get_settings()
        self.__get_settings_local()
        set_project_platform_activated_flag()

    def tearDown(self):
        try:
            os.remove(platform_settings_full_path())
        except Exception:
            pass
        try:
            os.remove(local_platform_settings_full_path())
        except Exception:
            pass
        super().tearDown()

    def __get_settings(self):
        with open(platform_settings_full_path()) as f:
            content = Template(f.read()).render(**get_template_vars_no_db())
            self.settings = yaml.full_load(content) or {}
            return self.settings

    def __get_settings_local(self):
        with open(local_platform_settings_full_path()) as f:
            content = Template(f.read()).render(**get_template_vars_no_db())
            self.settings_local = yaml.full_load(content) or {}
            return self.settings_local

    def test_activate_project(self):
        self.assertTrue(self.settings_local['projects']['bigbytes_platform']['active'])
        activate_project('bigbytes_data')

        self.__get_settings()
        self.__get_settings_local()

        self.assertFalse(self.settings_local['projects']['bigbytes_platform']['active'])
        self.assertTrue(self.settings_local['projects']['bigbytes_data']['active'])

    def test_get_repo_paths_for_file_path(self):
        self.assertEqual(
            get_repo_paths_for_file_path('bigbytes_platform/data_loaders/load.py'),
            dict(
                full_path=os.path.join(base_repo_path(), 'bigbytes_platform'),
                full_path_relative='test/bigbytes_platform',
                path='bigbytes_platform',
                root_project_full_path=base_repo_path(),
                root_project_name='test',
                uuid='bigbytes_platform',
            ),
        )

        self.assertEqual(
            get_repo_paths_for_file_path(
                'bigbytes_data/platform/data_loaders/bigbytes/fire/water/ice/load.py',
            ),
            dict(
                full_path=os.path.join(base_repo_path(), 'bigbytes_data/platform'),
                full_path_relative='test/bigbytes_data/platform',
                path='bigbytes_data/platform',
                root_project_full_path=base_repo_path(),
                root_project_name='test',
                uuid='bigbytes_data',
            ),
        )

    def test_build_active_project_repo_path(self):
        self.assertEqual(
            build_active_project_repo_path(),
            os.path.join(base_repo_path(), 'bigbytes_platform'),
        )
        activate_project('bigbytes_data')
        self.assertEqual(
            build_active_project_repo_path(),
            os.path.join(base_repo_path(), 'bigbytes_data/platform'),
        )

    def test_build_active_project_repo_path_no_active_projects(self):
        os.remove(local_platform_settings_full_path())
        # Reset project_platform_activated_flag
        set_project_platform_activated_flag()
        self.assertFalse(os.path.exists(local_platform_settings_full_path()))
        self.assertEqual(
            build_active_project_repo_path(),
            os.path.join(base_repo_path(), 'bigbytes_platform'),
        )

    def test_project_platform_activated(self):
        self.assertTrue(project_platform_activated())
        os.remove(platform_settings_full_path())
        # Reset project_platform_activated_flag
        set_project_platform_activated_flag()
        self.assertFalse(project_platform_activated())

    def test_platform_settings(self):
        settings = platform_settings()
        projects = settings['projects']
        self.assertEqual(projects['bigbytes_platform'], dict(
            database=SETTINGS['projects']['bigbytes_platform']['database'],
            git=SETTINGS['projects']['bigbytes_platform']['git'],
        ))
        self.assertEqual(projects['bigbytes_data'], dict(
            git=SETTINGS['projects']['bigbytes_data']['git'],
            path='bigbytes_data/platform',
        ))

    def test_active_project_settings(self):
        self.assertEqual(active_project_settings(), dict(
            active=True,
            database=SETTINGS['projects']['bigbytes_platform']['database'],
            git=SETTINGS['projects']['bigbytes_platform']['git'],
            uuid='bigbytes_platform',
        ))
        activate_project('bigbytes_data')
        self.assertEqual(active_project_settings(), dict(
            active=True,
            git=SETTINGS['projects']['bigbytes_data']['git'],
            path='bigbytes_data/platform',
            uuid='bigbytes_data',
        ))

    def test_project_platform_settings(self):
        self.assertEqual(project_platform_settings(bigbytes_projects_only=True), dict(
            bigbytes_platform=dict(
                active=True,
                database=SETTINGS['projects']['bigbytes_platform']['database'],
                git=SETTINGS['projects']['bigbytes_platform']['git'],
            ),
            bigbytes_data=dict(
                git=SETTINGS['projects']['bigbytes_data']['git'],
                path='bigbytes_data/platform',
            ),
        ))

    def test_git_settings(self):
        activate_project('bigbytes_data')
        self.assertEqual(git_settings(), dict(
            path=os.path.join(base_repo_path(), 'bigbytes_data/dev'),
        ))
        activate_project('bigbytes_platform')
        self.assertEqual(git_settings(), dict(
            path=os.path.join(base_repo_path(), 'bigbytes_platform', 'git'),
        ))

    def test_platform_settings_full_path(self):
        self.assertEqual(
            platform_settings_full_path(), os.path.join(base_repo_path(), 'settings.yaml'),
        )

    def test_local_platform_settings_full_path(self):
        self.assertEqual(
            local_platform_settings_full_path(), os.path.join(base_repo_path(), '.settings.yaml'),
        )

    def test_get_repo_path(self):
        from bigbytes.settings.repo import get_repo_path

        self.assertEqual(get_repo_path(), os.path.join(base_repo_path(), 'bigbytes_platform'))
        self.assertEqual(get_repo_path(absolute_path=False), 'test/bigbytes_platform')

        self.assertEqual(get_repo_path(root_project=True), base_repo_path())
        self.assertEqual(get_repo_path(root_project=True, absolute_path=False), 'test')

        file_path = os.path.join(base_repo_path(), 'bigbytes_data/platform/data_loaders/load.py')
        self.assertEqual(
            get_repo_path(file_path=file_path),
            os.path.join(base_repo_path(), 'bigbytes_data/platform'),
        )
        self.assertEqual(
            get_repo_path(file_path=file_path, absolute_path=False),
            'test/bigbytes_data/platform',
        )

        self.assertEqual(
            get_repo_path(file_path=file_path, root_project=True),
            base_repo_path(),
        )
        self.assertEqual(
            get_repo_path(file_path=file_path, root_project=True, absolute_path=False),
            'test',
        )

    def test_get_metadata_path(self):
        from bigbytes.settings.repo import get_metadata_path

        self.assertEqual(
            get_metadata_path(),
            os.path.join(base_repo_path(), 'bigbytes_platform/metadata.yaml'),
        )
        self.assertEqual(
            get_metadata_path(root_project=True),
            os.path.join(base_repo_path(), 'metadata.yaml'),
        )

        activate_project('bigbytes_data')
        self.assertEqual(
            get_metadata_path(),
            os.path.join(base_repo_path(), 'bigbytes_data/platform/metadata.yaml'),
        )
        self.assertEqual(
            get_metadata_path(root_project=True),
            os.path.join(base_repo_path(), 'metadata.yaml'),
        )

    def test_get_variables_dir(self):
        from bigbytes.settings.repo import get_variables_dir

        self.assertEqual(get_variables_dir(), os.path.join(base_repo_path(), 'bigbytes_platform'))
        self.assertEqual(
            get_variables_dir(os.path.join(base_repo_path(), 'bigbytes_data/platform')),
            os.path.join(base_repo_path(), 'bigbytes_data/platform'),
        )

        activate_project('bigbytes_data')
        self.assertEqual(get_variables_dir(), os.path.join(base_repo_path(), 'bigbytes_data/platform'))
        self.assertEqual(
            get_variables_dir(os.path.join(base_repo_path(), 'bigbytes_platform')),
            os.path.join(base_repo_path(), 'bigbytes_platform'),
        )

    def test_build_repo_path_for_all_projects(self):
        self.assertEqual(build_repo_path_for_all_projects(bigbytes_projects_only=True), dict(
            bigbytes_data=dict(
                full_path=os.path.join(base_repo_path(), 'bigbytes_data/platform'),
                full_path_relative='test/bigbytes_data/platform',
                path='bigbytes_data/platform',
                root_project_full_path=base_repo_path(),
                root_project_name='test',
                uuid='bigbytes_data',
            ),
            bigbytes_platform=dict(
                full_path=os.path.join(base_repo_path(), 'bigbytes_platform'),
                full_path_relative='test/bigbytes_platform',
                path='bigbytes_platform',
                root_project_full_path=base_repo_path(),
                root_project_name='test',
                uuid='bigbytes_platform',
            ),
        ))

    def test_repo_path_from_database_query_to_project_repo_path(self):
        self.assertEqual(
            repo_path_from_database_query_to_project_repo_path('pipeline_schedules'),
            {
                os.path.join(
                    os.path.dirname(base_repo_path()),
                    'default_repo',
                ): os.path.join(base_repo_path(), 'bigbytes_platform'),
                os.path.join(
                    os.path.dirname(base_repo_path()),
                    'default_repo/default_repo',
                ): os.path.join(base_repo_path(), 'bigbytes_platform'),
                os.path.join(
                    base_repo_path(),
                    'bigbytes_data/platform',
                ): os.path.join(base_repo_path(), 'bigbytes_data/platform'),
                os.path.join(
                    base_repo_path(),
                    'bigbytes_platform',
                ): os.path.join(base_repo_path(), 'bigbytes_platform'),
            },
        )
        self.assertEqual(
            repo_path_from_database_query_to_project_repo_path('secrets'),
            {
                os.path.join(
                    os.path.dirname(base_repo_path()),
                    'default_repo2',
                ): os.path.join(base_repo_path(), 'bigbytes_platform'),
                os.path.join(
                    os.path.dirname(base_repo_path()),
                    'default_repo2/default_repo',
                ): os.path.join(base_repo_path(), 'bigbytes_platform'),
                os.path.join(
                    base_repo_path(),
                    'bigbytes_data/platform',
                ): os.path.join(base_repo_path(), 'bigbytes_data/platform'),
                os.path.join(
                    base_repo_path(),
                    'bigbytes_platform',
                ): os.path.join(base_repo_path(), 'bigbytes_platform'),
            },
        )
