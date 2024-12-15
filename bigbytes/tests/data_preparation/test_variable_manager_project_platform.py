from unittest.mock import patch

from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.data_preparation.variable_manager import (
    get_global_variable,
    get_global_variables,
)
from bigbytes.tests.shared.mixins import ProjectPlatformMixin


@patch('bigbytes.data_preparation.models.pipeline.project_platform_activated', lambda: True)
@patch('bigbytes.data_preparation.variable_manager.project_platform_activated', lambda: True)
class VariableManagerProjectPlatformTests(ProjectPlatformMixin):
    def test_get_global_variable(self):
        for settings in self.repo_paths.values():
            pipeline = Pipeline.create(
                self.faker.unique.name(),
                repo_path=settings["full_path"],
            )
            value = self.faker.unique.name()
            pipeline.variables = dict(bigbytes=value)
            pipeline.save()

            self.assertEqual(get_global_variable(pipeline.uuid, "bigbytes"), value)

    def test_get_global_variables(self):
        for settings in self.repo_paths.values():
            pipeline = Pipeline.create(
                self.faker.unique.name(),
                repo_path=settings["full_path"],
            )
            pipeline.variables = self.faker.unique.name()
            pipeline.save()

            self.assertEqual(
                get_global_variables(None, pipeline=pipeline),
                pipeline.variables,
            )
            self.assertEqual(
                get_global_variables(pipeline.uuid), pipeline.variables
            )
