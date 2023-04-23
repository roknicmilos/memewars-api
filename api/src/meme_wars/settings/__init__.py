from meme_wars.settings.core import *  # noqa: F403
from meme_wars.settings.third_party import *  # noqa: F403
from meme_wars.settings.custom import *  # noqa: F403


INSTALLED_APPS += [
    *THIRD_PARTY_APPS,
    *CUSTOM_APPS,
]

MIDDLEWARE += THIRD_PARTY_MIDDLEWARE
