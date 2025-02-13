{% extends "data_loaders/default.jinja" %}
{% block imports %}
from bigbytes.data_preparation.repo_manager import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.pinot import Pinot
from os import path
{{ super() -}}
{% endblock %}


{% block content %}
@data_loader
def load_data_from_pinot(*args, **kwargs):
    """
    Template for loading data from a Pinot warehouse.
    Specify your configuration settings in 'io_config.yaml'.
    Docs: https://docs.bigbytes.ai/design/data-loading#pinot
    """
    query = 'your Pinot query'  # Specify your SQL query here
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Pinot.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)
{% endblock %}
