import os

__all__ = [
    'BASE_DIR',
    'base_path',
    'env_bool',
    'env_str',
    'env_int',
    'env_list',
    'load_env_file',
]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


def base_path(*args):
    """Path relative to project base directory"""
    return os.path.join(BASE_DIR, *args)


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
