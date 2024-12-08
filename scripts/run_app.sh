#!/bin/bash
set -eo pipefail

PROJECT_PATH="default_repo"
BIGBYTES_PROJECT_TYPE="standalone"

if [[ ! -z "${FILESTORE_IP_ADDRESS}" && ! -z "${FILE_SHARE_NAME}" ]]; then
    echo "Mounting Cloud Filestore ${FILESTORE_IP_ADDRESS}:/${FILE_SHARE_NAME}"
    mount -o nolock $FILESTORE_IP_ADDRESS:/$FILE_SHARE_NAME /home/src
    echo "Mounting completed."
fi

if [[ ! -z "${USER_CODE_PATH}" ]]; then
    PROJECT_PATH=$USER_CODE_PATH
fi

if [[ ! -z "${PROJECT_TYPE}" ]]; then
    BIGBYTES_PROJECT_TYPE=$PROJECT_TYPE
fi

if [[ ! -z "${ULIMIT_NO_FILE}" ]]; then
    echo "Setting ulimit -n  to $ULIMIT_NO_FILE"
    ulimit -n $ULIMIT_NO_FILE
fi

REQUIREMENTS_FILE="${PROJECT_PATH}/requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "$REQUIREMENTS_FILE exists."
    pip3 install -r $REQUIREMENTS_FILE
fi

bigbytes_args=()
if [[ ! -z "${PROJECT_UUID}" ]]; then
    bigbytes_args+=( '--project-uuid' "$PROJECT_UUID" )
fi

if [[ ! -z "${CLUSTER_TYPE}" ]]; then
    bigbytes_args+=( '--cluster-type' "$CLUSTER_TYPE" )
fi

if [ "$#" -gt 0 ]; then
    echo "Execute command: ${@}"
    "$@"
else
    echo "Starting project at ${PROJECT_PATH}, project type ${BIGBYTES_PROJECT_TYPE}"
    if [[ ! -z "${DBT_DOCS_INSTANCE}" ]]; then
        bigbytes start $PROJECT_PATH --dbt-docs-instance 1
    elif [[ ! -z "${MANAGE_INSTANCE}" ]]; then
        bigbytes start $PROJECT_PATH --manage-instance 1
    else
        bigbytes start $PROJECT_PATH --project-type $BIGBYTES_PROJECT_TYPE "${bigbytes_args[@]}"
    fi
fi
