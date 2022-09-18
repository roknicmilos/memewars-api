#!/bin/bash

set -e

. "$APP_ROOT_DIR"/scripts/load_env_vars.sh
. "$APP_ROOT_DIR"/scripts/colored_print.sh

initialize_django_project() {
  if [ "$APP_ENV" = 'development' ]; then
    printc "Starting project in $APP_ENV mode \n\n" "info"
    pip install -r "$APP_ROOT_DIR"/requirements/development.txt
    python "$APP_ROOT_DIR"/manage.py migrate
    python "$APP_ROOT_DIR"/manage.py collectstatic --noinput
    gunicorn -c "$APP_ROOT_DIR"/configs/gunicorn/development.py

  else
    printc "[ERROR]: Unknown environment: '$APP_ENV'. Available environment is 'development'.\n" "danger"
    printc "Exiting... \n\n"
    exit 1
  fi
}

load_environment_variables "$APP_ROOT_DIR"/.env
initialize_django_project "$@"
