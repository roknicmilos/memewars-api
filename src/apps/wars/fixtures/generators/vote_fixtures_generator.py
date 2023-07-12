from datetime import datetime, timedelta
from os.path import join
from random import randint

from django.conf import settings

from apps.common.fixtures import AbstractFixturesGenerator
from apps.common.utils import get_fixture_ids


class VoteFixturesGenerator(AbstractFixturesGenerator):
    raw_fixtures_item_template = """
        - model: wars.Vote
          pk: @pk
          fields:
            user: @user
            meme: @meme
            score: @score
            created: @dt
            modified: @dt
    """

    def __init__(self, *args, **kwargs):
        user_fixtures_file_path = join(settings.PROJECT_ROOT, "apps", "users", "fixtures", "users.yaml")
        self.user_ids = get_fixture_ids(fixtures_file_path=user_fixtures_file_path)
        meme_fixtures_file_path = join(settings.PROJECT_ROOT, "apps", "wars", "fixtures", "memes.yaml")
        self.meme_ids = get_fixture_ids(fixtures_file_path=meme_fixtures_file_path)
        super().__init__(*args, **kwargs)

    def get_fixture_items(self) -> list[dict]:
        items = []

        dt = datetime.now()
        for user_id in self.user_ids:
            for meme_id in self.meme_ids:
                dt_str = dt.isoformat().split(".")[0]
                items.append(
                    {
                        "pk": len(items) + 1,
                        "user": user_id,
                        "meme": meme_id,
                        "score": randint(1, 10),  # nosec B311
                        "dt": dt_str,
                    }
                )
                dt -= timedelta(seconds=1)

        return items
