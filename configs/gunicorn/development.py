# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "qwerty.wsgi:application"
# The granularity of Error logs outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 2
# The socket to bind
bind = "0.0.0.0:8000"
# Restart workers when code changes (development only!)
reload = True
# Write access and error info to /var/logs
accesslog = "./run/logs/gunicorn/qwerty.access.dev.logs"
errorlog = "./run/logs/gunicorn/qwerty.error.dev.logs"
# Redirect stdout/stderr to logs file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "./run/gunicorn/qwerty.dev.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = True
