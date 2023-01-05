#!/bin/sh

set -e

pwd
ls -la

. /app/scripts/colored_print.sh

wait_for_postgres() {
  # Adapted from https://docs.docker.com/compose/startup-order/
  echo 'Waiting for PostgreSQL...'
  until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOSTNAME" -U "$DB_USERNAME" -d "$DB_NAME" -c '\q'; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
  done
}

initialize_django_project() {
  if [ "$APP_ENV" = 'development' ]; then
    printc "Starting project in $APP_ENV mode \n\n" "info"
    python3 manage.py migrate
    python3 manage.py create_superuser --noinput
    python3 manage.py runserver 0.0.0.0:8000

  elif [ "$APP_ENV" = 'production' ]; then
    printc "Starting project in $APP_ENV mode \n\n" "info"
    python3 manage.py collectstatic --noinput
    python3 manage.py migrate
    python3 manage.py runserver 0.0.0.0:8000

  else
    printc "[ERROR]: Unknown environment: '$APP_ENV'. Available environments are 'development' and 'production'.\n" "danger"
    printc "Exiting... \n\n"
    exit 1
  fi
}

wait_for_postgres
initialize_django_project
