from os.path import join

from django.conf import settings
from django.core.management import BaseCommand

from apps.wars.utils import generate_vote_fixtures


class Command(BaseCommand):

    def handle(self, *args, **options):
        file_path = join(settings.PROJECT_ROOT, 'apps', 'wars', 'fixtures', 'votes.yaml')
        generated_fixtures = generate_vote_fixtures()
        with open(file_path, 'w') as file:
            file.write(generated_fixtures)
        self.stdout.write(self.style.SUCCESS(f'Generated Vote fixtures in {file_path}'))
