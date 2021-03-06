# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV boxid='2306ddb0-67d6-40d7-8099-17190977f6f0'
ENV tagfilter='messagetype,badge_event'

ENV db_server="10.100.100.150"
ENV db_user="piot_user_test"
ENV db_password="UIRcUQFWfnA8uasI4IGM"
ENV db_dbname="ocTerminal40_TEST"
ENV db_tablename="[oc_terminal_user_test].[terminal_entry]"

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install prerequisites
RUN apt-get update && apt-get install -y \
curl \
gnupg2 \
g++

#add keys and repo from microsoft for pyodbc
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && ACCEPT_EULA=Y apt-get -y install --no-install-recommends \
        msodbcsql17 \
        unixodbc-dev \
        git-all
        
#change ssl seclevel back to 1 to work with older certs.. 
RUN sed -i 's/CipherString = DEFAULT@SECLEVEL=2/CipherString = DEFAULT@SECLEVEL=1/' /etc/ssl/openssl.cnf

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "ldc_timedb_sync.py"]
