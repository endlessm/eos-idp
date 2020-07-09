from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import CommandError
import os


class Command(createsuperuser.Command):
    help = 'Ensure superuser exists.'

    def handle(self, *args, **options):
        if options['interactive']:
            raise CommandError('Can only run non-interactively')

        try:
            super().handle(*args, **options)
        except CommandError:
            username = options[self.UserModel.USERNAME_FIELD]
            if username is None:
                username_env_var = ('DJANGO_SUPERUSER_' +
                                    self.UserModel.USERNAME_FIELD.upper())
                username = os.environ[username_env_var]

            user = self.UserModel.objects.using(options['database']).get(
                **{self.UserModel.USERNAME_FIELD: username})

            user.is_staff = True
            user.is_superuser = True

            password = os.environ['DJANGO_SUPERUSER_PASSWORD']
            user.set_password(password)

            for field_name in self.UserModel.REQUIRED_FIELDS:
                env_var = 'DJANGO_SUPERUSER_' + field_name.upper()
                value = options[field_name] or os.environ[env_var]
                field = self.UserModel._meta.get_field(field_name)
                setattr(user, field_name, field.clean(value, None))

            user.save()

            if options['verbosity'] >= 1:
                self.stdout.write("Superuser updated successfully.")
