from os import path

from pandas import DataFrame

from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.oracledb import OracleDB

if 'data_exporter' not in globals():
    from bigbytes.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_oracledb(df: DataFrame, **kwargs) -> None:
    """
    Template to export data to Oracledb.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    table_name = 'your_table_name'

    with OracleDB.with_config(ConfigFileLoader(config_path, config_profile)) as exporter:
        exporter.export(
            df,
            table_name=table_name,
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
