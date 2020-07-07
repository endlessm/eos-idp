from Cryptodome.PublicKey import RSA
from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS, IntegrityError, router
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate, sender=global_apps.get_app_config('oidc_provider'))
def ensure_rsakey(app_config, verbosity=2, interactive=True,
                  using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    """Ensure an RSA key exists for token signing

    If no RSAKey objects exist, create one. This is registered as a
    post-migrate signal handler for the oidc_provider app so that it can
    be run immediately after the initial migration.
    """
    try:
        RSAKey = apps.get_model('oidc_provider', 'RSAKey')
    except LookupError:
        return

    if not router.allow_migrate_model(using, RSAKey):
        return

    if RSAKey.objects.using(using).exists():
        return

    if verbosity >= 1:
        print('Creating initial RSAKey')
    key = RSA.generate(2048).exportKey('PEM').decode('utf-8')
    try:
        RSAKey.objects.using(using).create(pk=1, key=key)
    except IntegrityError:
        pass
