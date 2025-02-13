import os
import shutil
import uuid
from unittest.mock import patch

import yaml

from bigbytes.data_preparation.repo_manager import (
    RepoConfig,
    get_project_uuid,
    get_repo_config,
    init_project_uuid,
    set_project_uuid_from_metadata,
)
from bigbytes.settings.repo import BIGBYTES_DATA_DIR_ENV_VAR
from bigbytes.tests.base_test import DBTestCase


def mock_uuid_value():
    return uuid.UUID('12345678123456781234567812345678')


class RepoManagerTest(DBTestCase):
    def test_variables_dir(self):
        if os.getenv(BIGBYTES_DATA_DIR_ENV_VAR):
            del os.environ[BIGBYTES_DATA_DIR_ENV_VAR]
        config_dict = dict(
            variables_dir='variables_dir_from_config_dict',
        )

        test1 = RepoConfig(repo_path=self.repo_path, config_dict=config_dict)
        self.assertEqual(
            test1.variables_dir,
            os.path.join(self.repo_path, 'variables_dir_from_config_dict'),
        )
        shutil.rmtree(test1.variables_dir)

        metadata_dict = dict(
            variables_dir='variables_dir_from_metadata',
        )
        test_repo_path = os.path.join(self.repo_path, 'repo_manager_test')
        os.makedirs(test_repo_path, exist_ok=True)
        with open(os.path.join(test_repo_path, 'metadata.yaml'), 'w') as f:
            yaml.dump(metadata_dict, f)
        test2 = RepoConfig(repo_path=test_repo_path)
        self.assertEqual(
            test2.variables_dir,
            os.path.join(test_repo_path, 'variables_dir_from_metadata'),
        )
        shutil.rmtree(test2.variables_dir)

        os.environ[BIGBYTES_DATA_DIR_ENV_VAR] = 'variables_dir_from_env_var'
        test4 = RepoConfig(repo_path=self.repo_path)
        self.assertEqual(
            test4.variables_dir,
            os.path.join(self.repo_path, 'variables_dir_from_env_var'),
        )
        del os.environ[BIGBYTES_DATA_DIR_ENV_VAR]
        shutil.rmtree(test4.variables_dir)

    def test_variables_dir_default(self):
        test = RepoConfig(repo_path=os.path.join(self.repo_path, 'non_existing_path'))
        self.assertEqual(
            test.variables_dir,
            os.path.join(self.repo_path, 'non_existing_path')
        )
        shutil.rmtree(test.variables_dir)

    def test_pipelines(self):
        test = RepoConfig(repo_path=os.path.join(self.repo_path, 'non_existing_path'))
        test.pipelines = dict(
            settings=dict(
                triggers=dict(
                    save_in_code_automatically=True,
                ),
            ),
        )
        self.assertTrue(test.pipelines.settings.triggers.save_in_code_automatically)

    def test_variables_dir_expanduser(self):
        dir_name = uuid.uuid4().hex
        metadata_dict = dict(
            variables_dir=os.path.join('~', dir_name),
        )
        test_repo_path = os.path.join(self.repo_path, 'repo_manager_test')
        os.makedirs(test_repo_path, exist_ok=True)
        with open(os.path.join(test_repo_path, 'metadata.yaml'), 'w') as f:
            yaml.dump(metadata_dict, f)
        test = RepoConfig(repo_path=test_repo_path)
        self.assertEqual(
            test.variables_dir,
            os.path.expanduser(os.path.join('~', dir_name, 'repo_manager_test'))
        )
        test_dir = os.path.expanduser(os.path.join('~', dir_name))
        shutil.rmtree(test_dir)

    def test_set_project_uuid_from_metadata(self):
        test_metadata_file = os.path.join(self.repo_path, 'metadata.yaml')
        with open(test_metadata_file, 'w', encoding='utf-8') as f:
            yaml.dump(dict(project_uuid='123456789'), f)

        set_project_uuid_from_metadata()
        self.assertEqual(get_project_uuid(), '123456789')
        # Reset the project metadata.yaml
        with open(os.path.join(self.repo_path, 'metadata.yaml'), 'w', encoding='utf-8') as f:
            yaml.dump(dict(), f)
            set_project_uuid_from_metadata()

    @patch('uuid.uuid4')
    def test_init_project_uuid(self, mock_uuid):
        mock_uuid.return_value = mock_uuid_value()
        # Reset the project metadata.yaml
        with open(os.path.join(self.repo_path, 'metadata.yaml'), 'w', encoding='utf-8') as f:
            yaml.dump(dict(), f)
            set_project_uuid_from_metadata()

        init_project_uuid()
        self.assertEqual(get_project_uuid(), mock_uuid_value().hex)

        os.remove(get_repo_config().metadata_path)

    def test_init_project_uuid_with_overwrite(self):
        metadata_path = get_repo_config().metadata_path
        with open(metadata_path, 'w', encoding='utf-8') as f:
            yaml.dump(dict(project_uuid='8888888888'), f)

        set_project_uuid_from_metadata()
        self.assertEqual(get_project_uuid(), '8888888888')

        init_project_uuid(overwrite_uuid='000000')
        self.assertEqual(get_project_uuid(), '000000')

        os.remove(metadata_path)
