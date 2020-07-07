import dj_database_url
import os
import hvac

__all__ = [
    'BASE_DIR',
    'base_path',
    'database_config',
    'env_bool',
    'env_str',
    'env_int',
    'env_list',
    'load_env_file',
    'Vault',
]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def base_path(*args):
    """Path relative to project base directory"""
    return os.path.join(BASE_DIR, *args)


def _build_database_url(vault):
    url = env_str('DATABASE_URL')
    if url:
        return url

    url = ''
    engine = vault.env_secret_str('DATABASE_ENGINE', 'database', 'engine')
    if not engine:
        return None
    url += f'{engine}://'

    user = vault.env_secret_str('DATABASE_USER', 'database', 'user')
    password = vault.env_secret_str('DATABASE_PASSWORD', 'database',
                                    'password')
    if user and password:
        url += f'{user}:{password}@'

    host = vault.env_secret_str('DATABASE_HOST', 'database', 'host')
    if host:
        url += f'{host}'

    url += '/'

    name = vault.env_secret_str('DATABASE_NAME', 'database', 'name')
    if name:
        url += f'{name}'

    options = vault.env_secret_str('DATABASE_OPTIONS', 'database', 'options')
    if options:
        url += '?{options}'

    return url


def database_config(vault, default):
    """Build database configuration

    If DATABASE_URL is not set, it can be composed from DATABASE_ENGINE,
    DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT and
    DATABASE_OPTIONS environment variables or vault.
    """
    url = _build_database_url(vault)
    if not url:
        url = default
    return dj_database_url.parse(url)


def str_to_bool(value, default=False):
    value = value.lower()
    if value in ('true', 'yes', '1'):
        return True
    elif value in ('false', 'no', '0'):
        return False
    else:
        return default


def env_bool(name, default=False):
    """
    Get a boolean value from environment variable.

    If the environment variable is not set or value is not one or "true" or
    "false", the default value is returned instead.
    """
    if name not in os.environ:
        return default
    return str_to_bool(os.environ[name], default)


def env_str(name, default=''):
    """
    Get a string value from environment variable.

    If the environment variable is not set, the default value is returned
    instead.
    """
    return os.environ.get(name, default)


def env_int(name, default=0):
    """
    Get an integer value from environment variable.

    If the environment variable is not set, the default value is returned
    instead.
    """
    return int(os.environ.get(name, default))


def env_list(name, default=None, separator=None):
    """
    Get a list of string values from environment variable.

    If the environment variable is not set, the default value is returned
    instead.
    """
    if default is None:
        default = []

    if name not in os.environ:
        return default
    return os.environ[name].split(separator)


def load_env_file(path=None):
    """Load an environment variable file

    Reads variable settings from a file and sets them in the environment when
    they are not already set. By default, a .env file at in the base directory
    is read.
    """
    if path is None:
        path = base_path('.env')
    if not os.path.isfile(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k, v)


class VaultError(Exception):
    """Errors from Vault secret handling"""
    pass


class Vault(object):
    """Vault secret manager

    If the VAULT_ADDR environment variable is set to the URL of a Vault
    server, a client will be created. A token for reading secrets can
    either be set through the VAULT_TOKEN environment variable or
    through the ~/.vault-token file as used by the vault CLI.
    """
    def __init__(self, address=None, secret_path=None):
        self.address = address or os.environ.get('VAULT_ADDR')
        self.secret_path = secret_path or os.environ.get('VAULT_SECRET_PATH')
        self.client = self._connect_client()

    def get_secret(self, path):
        """Get a secret from vault

        If a client hasn't been authenticated or the secret doesn't
        exist, None is returned. Otherwise, a dictionary of the secret
        data is returned.
        """
        if not self.client:
            return None
        full_path = os.path.join(self.secret_path, path)
        print(f'Reading vault secret "{full_path}"')
        resp = self.client.read(full_path)
        return resp.get('data', {}) if resp else None

    def get_secret_key(self, path, key, default=None):
        """Get a secret value at path:key from vault

        Returns the default if the secret or key don't exist.
        """
        secret = self.get_secret(path)
        return secret.get(key, default) if secret else default

    def secret_bool(self, path, key, default=False):
        """Get a boolean secret value at path:key from vault

        Returns the default if the secret or key don't exist.
        """
        value = self.get_secret_key(path, key, default)
        if isinstance(value, str):
            return str_to_bool(value, default)
        else:
            return bool(value)

    def secret_str(self, path, key, default=''):
        """Get a string secret value at path:key from vault

        Returns the default if the secret or key don't exist.
        """
        return str(self.get_secret_key(path, key, default))

    def secret_int(self, path, key, default=0):
        """Get an integer secret value at path:key from vault

        Returns the default if the secret or key don't exist.
        """
        return int(self.get_secret_key(path, key, default))

    def secret_list(self, path, key, default=None, separator=None):
        """Get a list secret value at path:key from vault

        Returns the default if the secret or key don't exist. If the
        secret value is a string, it will be split by separator.
        """
        if default is None:
            default = []
        value = self.get_secret_key(path, key)
        if value is None:
            return default
        elif isinstance(value, str):
            return value.split(separator)
        else:
            return value

    def env_secret_bool(self, env, path, key, default=False):
        """Get a boolean value from environment or secret"""
        if env in os.environ:
            return env_bool(env, default)
        else:
            return self.secret_bool(path, key, default)

    def env_secret_str(self, env, path, key, default=''):
        """Get a string value from environment or secret"""
        if env in os.environ:
            return env_str(env, default)
        else:
            return self.secret_str(path, key, default)

    def env_secret_int(self, env, path, key, default=0):
        """Get an integer value from environment or secret"""
        if env in os.environ:
            return env_int(env, default)
        else:
            return self.secret_int(path, key, default)

    def env_secret_list(self, env, path, key, default=None, separator=None):
        """Get a list value from environment or secret"""
        if env in os.environ:
            return env_list(env, default)
        else:
            return self.secret_list(path, key, default)

    def _connect_client(self):
        if self.address is None or self.secret_path is None:
            return None

        client = None
        token = os.environ.get('VAULT_TOKEN')
        token_file = os.path.expanduser('~/.vault-token')
        if token:
            print('Authenticating to vault with VAULT_TOKEN')
        elif os.path.exists(token_file):
            print(f'Authenticating to vault with {token_file}')
            with open(token_file, 'r') as f:
                token = f.read()

        if token:
            print(f'Connecting to vault server {self.address}')
            client = hvac.Client(url=self.address, token=token)
            if not client.is_authenticated():
                raise VaultError('Could not authenticate to vault')

        return client
