from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.duckdb import DuckDB
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from bigbytes.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_duckdb(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to DuckDB database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.bigbytes.io/design/data-loading#duckdb
    """
    table_name = 'your_table_name'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with DuckDB.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            None,
            table_name=table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
