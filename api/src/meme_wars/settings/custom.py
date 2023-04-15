from os import getenv


FIXTURES = (
    'users',
    'wars',
    'memes',
    'votes',
)

GOOGLE_OPENID_CONFIG_URL = 'https://accounts.google.com/.well-known/openid-configuration'
GOOGLE_OPENID_CLIENT_ID = getenv('GOOGLE_OPENID_CLIENT_ID')
GOOGLE_OPENID_CLIENT_SECRET = getenv('GOOGLE_OPENID_CLIENT_SECRET')

HOST_URL = f'{getenv("WEB_API_BASE_URL")}:{getenv("WEB_API_PORT")}'

CLIENT_APP_URL = f'{getenv("WEB_APP_BASE_URL")}:{getenv("WEB_APP_PORT")}'
