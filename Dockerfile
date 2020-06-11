FROM python:3.8-slim AS build

RUN apt-get update && \
    apt-get -y install \
        build-essential \
        libpq-dev \
        && \
    apt-get clean

COPY requirements.txt /
RUN pip install --no-cache-dir --root /dest -r requirements.txt

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
WORKDIR /opt/eos-idp
COPY . .
RUN python -m compileall .

# Need to pass non-empty SECRET_KEY since it's empty by default
RUN SECRET_KEY=fake ./manage.py collectstatic -c --no-input

USER nobody
EXPOSE 8000
ENV WORKERS=2
ENV DATABASE_URL=sqlite:////tmp/db.sqlite3
ENTRYPOINT ["./entrypoint"]
CMD ["./run"]
