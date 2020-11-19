# Settings to be used during tests. This is not intended to be used at
# runtime.
from .base import *  # noqa

# Ensure SECRET_KEY is not empty
if not SECRET_KEY:
    SECRET_KEY = 'badsecret'
