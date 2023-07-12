from django.conf import settings
from django.core.management.commands.loaddata import Command as LoadDataCommand


class Command(LoadDataCommand):
    missing_args_message = (
        f"{LoadDataCommand.missing_args_message} Alternatively, "
        "set FIXTURES collection (list or tuple) in the settings."
    )

    def run_from_argv(self, argv):
        prepared_argv = self.prepare_argv(argv=argv)
        super().run_from_argv(argv=prepared_argv)

    @classmethod
    def prepare_argv(cls, argv: list) -> list:
        contains_app_labels = bool(next((arg for arg in argv[2:] if not arg.startswith("-")), None))
        if not contains_app_labels:
            try:
                argv = argv[:2] + list(settings.FIXTURES) + argv[2:]
            except AttributeError:
                pass

        return argv
