from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.snowflake import Snowflake
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from bigbytes.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_snowflake(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Snowflake warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.bigbytes.io/design/data-loading#snowflake
    """
    table_name = 'your_table_name'
    database = 'your_database_name'
    schema = 'your_schema_name'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Snowflake.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            table_name,
            database,
            schema,
            if_exists='replace',  # Specify resolution policy if table already exists
        )
