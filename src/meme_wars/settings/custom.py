from decouple import config


CUSTOM_APPS = [
    'apps.common',
    'apps.users',
    'apps.wars',
]

FIXTURES = (
    'users',
    'wars',
    'memes',
    'votes',
)

GOOGLE_OPENID_CONFIG_URL = 'https://accounts.google.com/.well-known/openid-configuration'
GOOGLE_OPENID_CLIENT_ID = config('GOOGLE_OPENID_CLIENT_ID')
GOOGLE_OPENID_CLIENT_SECRET = config('GOOGLE_OPENID_CLIENT_SECRET')

HOST_URL = config('API_BASE_URL')
