from django.conf import settings
from django.core.management.commands.loaddata import Command as LoadDataCommand


class Command(LoadDataCommand):
    missing_args_message = (
        f'{LoadDataCommand.missing_args_message} Alternatively, '
        f'set FIXTURES collection (list or tuple) in the settings.'
    )

    def run_from_argv(self, argv):
        fixtures = [arg for arg in argv[2:] if not arg.startswith('-')]
        if not fixtures:
            try:
                argv = argv[:2] + list(settings.FIXTURES) + argv[2:]
            except AttributeError:
                pass
        super(Command, self).run_from_argv(argv)
