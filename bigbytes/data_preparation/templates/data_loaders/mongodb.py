{% extends "data_loaders/default.jinja" %}
{% block imports %}
from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.mongodb import MongoDB
from os import path
{{ super() -}}
{% endblock %}


{% block content %}
@data_loader
def load_from_mongodb(*args, **kwargs):
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    query = {}

    return MongoDB.with_config(ConfigFileLoader(config_path, config_profile)).load(
        query=query,
        collection='collection_name',
    )
{% endblock %}
