from os.path import join

from django.conf import settings
from django.core.management import BaseCommand

from apps.common.fixtures import AbstractFixturesGenerator
from apps.wars.fixtures.generators import MemeFixturesGenerator, VoteFixturesGenerator


class Command(BaseCommand):
    available_fixtures = ["votes", "memes"]
    help = 'Generates fixture files for "war" app that can be loaded into DB ' 'using "load_data" management command'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "args",
            metavar="fixtures",
            nargs="+",
            choices=self.available_fixtures,
            help="Fixture labels.",
        )
        parser.add_argument(
            "-ql",
            "--quantity-level",
            type=int,
            default=1,
            choices=[1, 2, 3],
            help=(
                "Level of the fixture items quantity that you want to generate. "
                "E.g. if there are 10 fixture items generated with quantity leve 1, "
                "there could be 20 fixture items generated using level 2."
                "The number of items for each quantity level depends on specific fixtures."
            ),
        )

    def handle(self, *args, **options):
        for fixtures_name in args:
            file_path = join(settings.PROJECT_ROOT, "apps", "wars", "fixtures", f"{fixtures_name}.yaml")
            fixtures_generator = _init_fixtures_generator(
                fixtures_name=fixtures_name, quantity_level=options["quantity_level"]
            )
            with open(file_path, "w") as file:
                file.write(fixtures_generator.generate())
            success_message = self.style.SUCCESS(
                f"Generated {fixtures_name} fixtures in {file_path} containing "
                f"{len(fixtures_generator.fixture_items)} fixture items"
            )
            self.stdout.write(success_message)


def _init_fixtures_generator(fixtures_name: str, quantity_level: int) -> AbstractFixturesGenerator:
    match fixtures_name:
        case "votes":
            return VoteFixturesGenerator(quantity_level=quantity_level)
        case "memes":
            return MemeFixturesGenerator(quantity_level=quantity_level)
