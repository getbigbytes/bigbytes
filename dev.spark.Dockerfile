FROM python:3.10-bookworm
LABEL description="Bigbytes data management platform"
ARG PIP=pip3
USER root

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Add Debian Bullseye repository
RUN echo 'deb http://deb.debian.org/debian bullseye main' > /etc/apt/sources.list.d/bullseye.list

## System Packages
RUN \
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
  NODE_MAJOR=20 && \
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
  apt-get -y update && \
  ACCEPT_EULA=Y apt-get -y install --no-install-recommends \
    # Node
    nodejs \
    # NFS dependencies
    nfs-common \
    # odbc dependencies
    msodbcsql18 \
    # Install OpenJDK 11
    openjdk-11-jdk \
    unixodbc-dev && \
    # R
    # r-base=4.2.2.20221110-2 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  # Remove Debian Bullseye repository
  rm /etc/apt/sources.list.d/bullseye.list

## R Packages
# RUN \
#   R -e "install.packages('pacman', repos='http://cran.us.r-project.org')" && \
#   R -e "install.packages('renv', repos='http://cran.us.r-project.org')"

## Node Packages
RUN npm install --global yarn && yarn global add next

## Python Packages
RUN \
  pip3 install --no-cache-dir sparkmagic && \
  mkdir ~/.sparkmagic && \
  curl https://raw.githubusercontent.com/jupyter-incubator/sparkmagic/master/sparkmagic/example_config.json > ~/.sparkmagic/config.json && \
  sed -i 's/localhost:8998/host.docker.internal:9999/g' ~/.sparkmagic/config.json && \
  jupyter-kernelspec install --user "$(pip3 show sparkmagic | grep Location | cut -d' ' -f2)/sparkmagic/kernels/pysparkkernel"
# Bigbytes integrations and other related packages
RUN \
  pip3 install --no-cache-dir "git+https://github.com/wbond/oscrypto.git@d5f3437ed24257895ae1edd9e503cfb352e635a8" && \
  pip3 install --no-cache-dir "git+https://github.com/digitranslab/singer-python.git#egg=singer-python" && \
  pip3 install --no-cache-dir "git+https://github.com/digitranslab/dbt-mysql.git#egg=dbt-mysql" && \
  pip3 install --no-cache-dir "git+https://github.com/digitranslab/dbt-synapse.git#egg=dbt-synapse" && \
  pip3 install --no-cache-dir pyspark
COPY bigbytes_integrations /tmp/bigbytes_integrations
RUN \
  pip3 install --no-cache-dir /tmp/bigbytes_integrations && \
  rm -rf /tmp/bigbytes_integrations
# Bigbytes Dependencies
COPY requirements.txt /tmp/requirements.txt
RUN \
  pip3 install --no-cache-dir -r /tmp/requirements.txt && \
  rm /tmp/requirements.txt

## Bigbytes Frontend
COPY ./bigbytes /home/src/bigbytes
WORKDIR /home/src/bigbytes/frontend
RUN yarn install && yarn cache clean

ENV BIGBYTES_DATA_DIR=
ENV PYTHONPATH="${PYTHONPATH}:/home/src"
WORKDIR /home/src
