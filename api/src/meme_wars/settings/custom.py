from decouple import config


FIXTURES = (
    'users',
    'wars',
    'memes',
    'votes',
)

GOOGLE_OPENID_CONFIG_URL = 'https://accounts.google.com/.well-known/openid-configuration'
GOOGLE_OPENID_CLIENT_ID = config('GOOGLE_OPENID_CLIENT_ID')
GOOGLE_OPENID_CLIENT_SECRET = config('GOOGLE_OPENID_CLIENT_SECRET')

HOST_URL = config('WEB_API_BASE_URL')

CLIENT_APP_URL = config('WEB_APP_BASE_URL')
