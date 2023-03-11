from datetime import datetime
from random import randint

from apps.common.fixtures import AbstractFixturesGenerator
from apps.users.models import User
from apps.wars.models import Meme


class VoteFixturesGenerator(AbstractFixturesGenerator):
    raw_fixture_template = """
        - model: wars.Vote
          pk: @pk
          fields:
            user: @user
            meme: @meme
            score: @score
            created: @now
            modified: @now
    """

    def generate(self) -> str:
        output = ''

        current_vote_id = 1
        for user in User.objects.exclude(pk=1).all():
            for meme in Meme.objects.filter(war__pk=1).all():
                output += self._render_vote_fixture(pk=current_vote_id, user=user, meme=meme)
                current_vote_id += 1

        return output

    def _render_vote_fixture(self, pk: int, user: User, meme: Meme) -> str:
        now_str = datetime.now().isoformat().split('.')[0]
        return self.fixture_template \
            .replace('@pk', str(pk)) \
            .replace('@user', str(user.pk)) \
            .replace('@meme', str(meme.pk)) \
            .replace('@score', str(randint(1, 10))) \
            .replace('@now', now_str)
