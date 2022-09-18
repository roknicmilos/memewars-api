from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            super(Command, self).handle(*args, **options)
        except Exception as error:
            self.stderr.write(f'{type(error).__name__}: "{str(error)}"')
