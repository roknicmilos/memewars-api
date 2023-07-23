from meme_wars.settings.core import *
from meme_wars.settings.custom import *
from meme_wars.settings.third_party import *

INSTALLED_APPS += [
    *THIRD_PARTY_APPS,
    *CUSTOM_APPS,
]

MIDDLEWARE += THIRD_PARTY_MIDDLEWARE
