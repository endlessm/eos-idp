# Settings to be used during builds. This is not intended to be used at
# runtime. Primarily it is to ensure that all applications are enabled
# for static file collection.
from .base import *  # noqa

# Ensure SECRET_KEY is not empty
if not SECRET_KEY:
    SECRET_KEY = 'badsecret'

# Include all supported socialaccount providers
for app in ('allauth.socialaccount.providers.google',
            'allauth.socialaccount.providers.facebook'):
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
