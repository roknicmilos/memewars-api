from os.path import join

from django.conf import settings
from django.core.management import BaseCommand

from apps.wars.fixtures import VoteFixturesGenerator


class Command(BaseCommand):
    help = 'Generates fixtures for Vote model based on the users currently present in DB'

    def handle(self, *args, **options):
        file_path = join(settings.PROJECT_ROOT, 'apps', 'wars', 'fixtures', 'votes.yaml')
        generated_fixtures = VoteFixturesGenerator().generate()
        with open(file_path, 'w') as file:
            file.write(generated_fixtures)
        self.stdout.write(self.style.SUCCESS(f'Generated Vote fixtures in {file_path}'))
