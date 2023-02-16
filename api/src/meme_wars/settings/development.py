# Common settings:
from .common import *  # noqa: F403

# uncomment the following line to include i18n
# from .i18n import *

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# adjust the minimal login
LOGIN_REDIRECT_URL = '/'

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS  # noqa: F405

CLIENT_APP['URL'] = 'http://localhost:3000'  # noqa: F405
