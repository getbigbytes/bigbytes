from os import path

from pandas import DataFrame

from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.chroma import Chroma

if 'data_exporter' not in globals():
    from bigbytes.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_chroma(df: DataFrame, **kwargs) -> None:
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    document_column = 'documents'
    new_collection = 'new_colletion'

    Chroma.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        collection=new_collection,
        document_column=document_column
    )
