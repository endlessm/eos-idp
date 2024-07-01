FROM docker.io/python:3.9-slim AS build

RUN apt-get update && \
    apt-get -y install \
        build-essential \
        libpq-dev \
        && \
    apt-get clean

COPY requirements.txt /
RUN pip install --no-cache-dir --root /dest --no-warn-script-location \
    -r requirements.txt

FROM docker.io/hashicorp/vault:latest AS vault

FROM docker.io/python:3.9-slim

RUN apt-get update && \
    apt-get -y install \
        ca-certificates \
        curl \
        libpq5 \
        && \
    apt-get clean

ADD https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem \
    /usr/local/share/ca-certificates/rds.crt
RUN update-ca-certificates

COPY --from=build /dest/ /
COPY --from=vault /bin/vault /usr/bin/
WORKDIR /opt/eos-idp
COPY . .
RUN python -m compileall .

# Need to use custom settings to ensure consistent apps and use a fake
# secret key.
RUN ./manage.py collectstatic -c --no-input --settings eosidp.settings.build

# Add user with real homedir since vault uses that
RUN adduser --system --group --home /run/eos-idp --shell /usr/sbin/nologin \
    eos-idp
USER eos-idp

EXPOSE 8000
ENV WORKERS=2
ENV DATABASE_ENGINE=sqlite
ENV DATABASE_NAME=/run/eos-idp/db.sqlite3
ENTRYPOINT ["./entrypoint"]
CMD ["./run"]
