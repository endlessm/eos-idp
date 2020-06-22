FROM python:3.8-slim AS build

RUN apt-get update && \
    apt-get -y install \
        build-essential \
        libpq-dev \
        && \
    apt-get clean

COPY requirements.txt /
RUN pip install --no-cache-dir --root /dest --no-warn-script-location \
    -r requirements.txt

FROM vault:latest AS vault

FROM python:3.8-slim

RUN apt-get update && \
    apt-get -y install \
        ca-certificates \
        libpq5 \
        && \
    apt-get clean

ADD https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem \
    /usr/local/share/ca-certificates/rds.crt
RUN update-ca-certificates

COPY --from=build /dest/ /
COPY --from=vault /bin/vault /usr/bin/
WORKDIR /opt/eos-idp
COPY . .
RUN python -m compileall .

# Need to pass non-empty SECRET_KEY since it's empty by default
RUN SECRET_KEY=fake ./manage.py collectstatic -c --no-input

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
