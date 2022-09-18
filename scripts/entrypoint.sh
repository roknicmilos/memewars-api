#!/bin/sh

set -e

. "$APP_ROOT_DIR"/scripts/colored_print.sh

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
    python3 "$APP_ROOT_DIR"/manage.py migrate
    python3 "$APP_ROOT_DIR"/manage.py collectstatic --noinput
    python3 manage.py loaddata users
    python3 manage.py create_superuser --noinput
    python3 manage.py runserver 0.0.0.0:8000

  else
    printc "[ERROR]: Unknown environment: '$APP_ENV'. Available environment is 'development'.\n" "danger"
    printc "Exiting... \n\n"
    exit 1
  fi
}

wait_for_postgres
initialize_django_project
