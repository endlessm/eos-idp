from Cryptodome.PublicKey import RSA
from django.apps import apps as global_apps
from django.conf import settings
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


@receiver(post_migrate, sender=global_apps.get_app_config('sites'))
def setup_site(app_config, verbosity=2, interactive=True,
               using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    """Setup Site details from settings

    Use the SITE_ID, SITE_DOMAIN and SITE_NAME settings to set the Site
    details for this project. The sites app automatically generates site
    ID 1, but it just uses example.com as the domain and name. This will
    update that site or create a new one if a different SITE_ID is
    specified.
    """
    if not all((settings.SITE_ID, settings.SITE_DOMAIN, settings.SITE_NAME)):
        return

    try:
        Site = apps.get_model('sites', 'Site')
    except LookupError:
        return

    if not router.allow_migrate_model(using, Site):
        return

    fields = {
        'domain': settings.SITE_DOMAIN,
        'name': settings.SITE_NAME,
    }
    site, created = Site.objects.using(using).update_or_create(
        id=settings.SITE_ID, defaults=fields)
    if verbosity >= 1:
        print('Created' if created else 'Updated', site.name, 'site')
