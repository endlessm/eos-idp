# Endless OS Identity Provider

eos-idp is an identity provider for Endless OS. It supplies an [OpenID
Connect][openid-connect] provider for authentication in client
applications. Authentication to eos-idp can be done with a traditional
username and password or via 3rd party authenticators such as Google.
eos-idp is built on [Django][django].

[openid-connect]: https://openid.net/connect/
[django]: https://www.djangoproject.com/

## Setup

Create a Python 3 virtual environment and install the requirements.

```
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

Most settings can be controlled by environment variables. Alternatively,
a `.env` file in the checkout can be used to populate the environment
variables. See the [`example.env`](example.env) file for documentation
on available variables. Further customization can be accomplished by
adding a [Django settings file][django-settings] at
`eosidp/settings/local.py`.

[django-settings]: https://docs.djangoproject.com/en/3.0/topics/settings/

For a quick setup, copy `example.env` to `.env` and edit it.

```
cp example.env .env
editor .env
```

Now create an adminstrator user and initialize the database tables.

```
./manage.py createsuperuser
./manage.py migrate
```

Before the OpenID Connect provider can be used, a keypair must be
created for signing the tokens.

```
./manage.py creatersakey
```

Now you can run the server.

```
./manage.py runserver
```

This will start Django's built-in WSGI server, but in a real deployment
[Gunicorn][gunicorn] is suggested.

```
gunicorn eosidp.wsgi
```

[gunicorn]: https://gunicorn.org/

## Clients

In order to use eos-idp as an authenticator, a client application must
be registered as an OpenID Connect Relying Party. See the
django-oidc-provider [documentation][relying-party] on how to register
clients.

[relying-party]: https://django-oidc-provider.readthedocs.io/en/latest/sections/relyingparties.html

## Deployment

A [`Dockerfile`](Dockerfile) is provided to build a container image for
eos-idp. First, build the image.

```
docker build -t eos-idp .
```

Now run it the container.

```
docker run --rm --env-file .env -p 8000:8000 eos-idp
```

## Development

Dependencies are managed with [Pipenv][pipenv] in the
[`Pipfile`](Pipfile). Run `pipenv install` to install a `virtualenv`
with the specified dependencies. Run `pipenv run test` to run the test
suite.

To update dependencies, make the appropriate changes to `Pipfile` and
run `pipenv lock`. For deployment convenience, a `requirements.txt` file
is maintained. This is generated from the versions in the `Pipfile.lock`
file. When updating dependencies, run `pipenv requirements >
requirements.txt`.

[pipenv]: https://pipenv.pypa.io/en/latest/
