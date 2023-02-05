from datetime import datetime
from random import randint
from apps.users.models import User
from apps.wars.models import Meme


def _prepare_vote_fixture_template() -> str:
    original_template = """
    - model: wars.Vote
      pk: @pk
      fields:
        user: @user
        meme: @meme
        score: @score
        created: @now
        modified: @now
    """

    original_template_without_empty_lines = "".join([
        line for line in original_template.splitlines(keepends=True) if line.strip()
    ])
    first_line = original_template_without_empty_lines.splitlines()[0]
    first_line_indent = len(first_line) - len(first_line.lstrip())

    prepared_template = ''
    for line in original_template_without_empty_lines.splitlines(keepends=True):
        prepared_template += line[first_line_indent:]

    return prepared_template


template = _prepare_vote_fixture_template()


def generate_vote_fixtures() -> str:
    output = ''

    current_vote_id = 1
    for user in User.objects.all():
        for meme in Meme.objects.filter(war__pk=1).all():
            output += _render_vote_fixture(pk=current_vote_id, user=user, meme=meme)
            current_vote_id += 1

    return output


def _render_vote_fixture(pk: int, user: User, meme: Meme) -> str:
    now_str = datetime.now().isoformat().split('.')[0]
    return template \
        .replace('@pk', str(pk)) \
        .replace('@user', str(user.pk)) \
        .replace('@meme', str(meme.pk)) \
        .replace('@score', str(randint(1, 10))) \
        .replace('@now', now_str)
