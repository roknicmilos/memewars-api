#!/bin/bash

set -e

printc () {
    if [ "$2" == "info" ] ; then
        COLOR="96m"; # light blue
    elif [ "$2" == "success" ] ; then
        COLOR="92m"; # green
    elif [ "$2" == "warning" ] ; then
        COLOR="93m"; # yellow
    elif [ "$2" == "danger" ] ; then
        COLOR="91m"; # red
    else
        COLOR="0m"; # no (default) color
    fi

    START_COLOR="\e[$COLOR";
    END_COLOR="\e[0m";
    printf "$START_COLOR%b$END_COLOR" "$1";
}

load_environment_variables() {
  printc "Loading environment variables...\n"

  # Show environment variables:
  grep -v '^#' .env

  # Export environment variables:
  export "$(grep -v '^#' .env | xargs)"
  printc "\n"
}

initialize_django_project() {
  if [ "$APP_ENV" = 'development' ]; then
    printc "Starting project in $APP_ENV mode \n\n" "info"
    python manage.py migrate
    python manage.py collectstatic --noinput
    gunicorn -c configs/gunicorn/development.py

  elif [ "$APP_ENV" = 'production' ]; then
    printc "Starting project in $APP_ENV mode \n\n" "info"
    python manage.py migrate
    python manage.py collectstatic --noinput
    gunicorn -c configs/gunicorn/production.py

  else
    printc "[ERROR]: Unknown environment: '$APP_ENV'. Available arguments are 'development' and 'production'.\n" "danger"
    printc "Exiting... \n\n"
    exit 1
  fi
}

load_environment_variables
initialize_django_project "$@"
