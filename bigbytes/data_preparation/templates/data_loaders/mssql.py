{% extends "data_loaders/default.jinja" %}
{% block imports %}
from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.mssql import MSSQL
from os import path
{{ super() -}}
{% endblock %}


{% block content %}
@data_loader
def load_data_from_mssql(*args, **kwargs):
    """
    Template for loading data from a MSSQL database.
    Specify your configuration settings in 'io_config.yaml'.
    Set the following in your io_config:

    Docs: https://docs.bigbytes.ai/integrations/databases/MicrosoftSQLServer
    """
    query = 'Your MSSQL query'  # Specify your SQL query here
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with MSSQL.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)
{% endblock %}
