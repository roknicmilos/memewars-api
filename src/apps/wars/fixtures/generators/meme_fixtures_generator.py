import os
import random
from datetime import datetime, timedelta
from os.path import join

from django.conf import settings

from apps.common.fixtures import AbstractFixturesGenerator
from apps.common.utils import get_fixture_ids


class MemeFixturesGenerator(AbstractFixturesGenerator):
    raw_fixtures_item_template = """
        - model: wars.Meme
          pk: @pk
          fields:
            user: @user
            war: @war
            image: fixtures/memes/@image
            approval_status: approved
            created: @dt
            modified: @dt
    """

    def __init__(self, *args, **kwargs):
        meme_fixtures_media_dir_path = join(settings.PROJECT_ROOT, "run", "media", "fixtures", "memes")
        self.meme_fixture_image_filenames = os.listdir(meme_fixtures_media_dir_path)
        user_fixtures_file_path = join(settings.PROJECT_ROOT, "apps", "users", "fixtures", "users.yaml")
        self.user_ids = get_fixture_ids(fixtures_file_path=user_fixtures_file_path)
        war_fixtures_file_path = join(settings.PROJECT_ROOT, "apps", "wars", "fixtures", "wars.yaml")
        self.war_ids = get_fixture_ids(fixtures_file_path=war_fixtures_file_path)
        super().__init__(*args, **kwargs)

    def get_fixture_items(self) -> list[dict]:
        items = []

        dt = datetime.now()
        for index in range(self.quantity_level):
            for war_id in self.war_ids:
                for image_filename in self.meme_fixture_image_filenames:
                    random_user_id = self.user_ids[random.randint(0, len(self.user_ids) - 1)]  # nosec B311
                    dt_str = dt.isoformat().split(".")[0]
                    items.append(
                        {
                            "pk": len(items) + 1,
                            "user": random_user_id,
                            "war": war_id,
                            "image": image_filename,
                            "dt": dt_str,
                        }
                    )
                    dt -= timedelta(seconds=1)

        return items
