import pandas as pd
from pandas.testing import assert_frame_equal

from bigbytes.data_preparation.models.block import Block
from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.data_preparation.models.variables.constants import VariableType
from bigbytes.data_preparation.repo_manager import get_repo_config
from bigbytes.data_preparation.variable_manager import (
    VariableManager,
    get_global_variable,
    set_global_variable,
)
from bigbytes.settings.repo import set_repo_path
from bigbytes.tests.base_test import DBTestCase


class VariableManagerTest(DBTestCase):
    def test_add_and_get_variable(self):
        self.__create_pipeline("test pipeline 1")
        variable_manager = VariableManager(
            variables_dir=get_repo_config(self.repo_path).variables_dir,
        )
        data1 = {"k1": "v1", "k2": "v2"}
        data2 = pd.DataFrame(
            [
                ["test1", 1],
                ["test2", 2],
            ],
            columns=["col1", "col2"],
        )
        data3 = dict(
            metadata=dict(
                column_types=dict(
                    col1="number",
                    col2="text",
                ),
            ),
            statistics=dict(
                count=100,
                count_distinct=50,
            ),
            insights=dict(),
            suggestions=[
                dict(
                    title="Remove outliers",
                )
            ],
        )
        variable_manager.add_variable("test_pipeline_1", "block1", "var1", data1)
        variable_manager.add_variable("test_pipeline_1", "block2", "var2", data2)
        variable_manager.add_variable(
            "test_pipeline_1",
            "block2",
            "var2",
            data3,
            variable_type=VariableType.DATAFRAME_ANALYSIS,
        )
        self.assertEqual(
            variable_manager.get_variable("test_pipeline_1", "block1", "var1"),
            data1,
        )
        assert_frame_equal(
            variable_manager.get_variable("test_pipeline_1", "block2", "var2"),
            data2,
        )
        self.assertEqual(
            variable_manager.get_variable(
                "test_pipeline_1",
                "block2",
                "var2",
                variable_type=VariableType.DATAFRAME_ANALYSIS,
            ),
            data3,
        )

    def test_get_variables_by_pipeline(self):
        self.__create_pipeline("test pipeline 2")
        variable_manager = VariableManager(
            repo_path=self.repo_path,
            variables_dir=get_repo_config(self.repo_path).variables_dir,
        )
        variable_manager.add_variable("test_pipeline_2", "block1", "var1", 1)
        variable_manager.add_variable("test_pipeline_2", "block1", "var2", 2)
        variable_manager.add_variable("test_pipeline_2", "block2", "var3", 3)
        variable_manager.add_variable("test_pipeline_2", "block2", "var4", 4)
        self.assertEqual(
            variable_manager.get_variables_by_pipeline("test_pipeline_2"),
            dict(block1=["var1", "var2"], block2=["var3", "var4"]),
        )

    def test_set_and_get_global_variable(self):
        set_repo_path(self.repo_path)
        self.__create_pipeline("test pipeline 3")
        set_global_variable("test_pipeline_3", "var1", 1)
        set_global_variable("test_pipeline_3", "var2", "test")
        set_global_variable("test_pipeline_3", "var3", [1, 2, 3])
        set_global_variable("test_pipeline_3", "var4", dict(k1="v1", k2="v2"))
        self.assertEqual(get_global_variable("test_pipeline_3", "var1"), 1)
        self.assertEqual(get_global_variable("test_pipeline_3", "var2"), "test")
        self.assertEqual(get_global_variable("test_pipeline_3", "var3"), [1, 2, 3])
        self.assertEqual(
            get_global_variable("test_pipeline_3", "var4"), dict(k1="v1", k2="v2")
        )

    def __create_pipeline(self, name):
        pipeline = Pipeline.create(
            name,
            repo_path=self.repo_path,
        )
        block1 = Block.create("block1", "data_loader", self.repo_path)
        block2 = Block.create("block2", "transformer", self.repo_path)
        pipeline.add_block(block1)
        pipeline.add_block(block2)
        return pipeline

    # def test_get_global_variables(self):
    #     pipeline = Pipeline.create(
    #         self.faker.unique.name(),
    #         repo_path=self.repo_path,
    #     )
    #     pipeline.variables = {'name': self.faker.unique.name()}
    #     pipeline.save()
    #     self.assertEqual(
    #         get_global_variables(None, pipeline=pipeline), pipeline.variables
    #     )
    #     self.assertEqual(get_global_variables(pipeline.uuid), pipeline.variables)
