FROM python:3.6-slim

# Install prerequisites
RUN apt-get update && apt-get install -y \
curl \
gnupg2

RUN pip install --no-cache-dir matplotlib pandas

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