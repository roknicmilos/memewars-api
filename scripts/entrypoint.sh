#!/bin/bash

set -e

. /app/scripts/utils.sh

wait_for_postgres() {
  # Adapted from https://docs.docker.com/compose/startup-order/
  printc "Waiting for PostgreSQL...\n" "info"
  until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOSTNAME" -U "$DB_USERNAME" -d "$DB_NAME" -c '\q'; do
    printc >&2 "Postgres is unavailable - sleeping" "info"
    sleep 1
  done
}

run_server() {
  if bool "$DEV_SERVER"; then
    printc "Starting Django development server...\n" "info"
    python3 manage.py runserver 0.0.0.0:8000
  else
    printc "Starting Gunicorn server...\n" "info"
    gunicorn meme_wars.wsgi --bind 0.0.0.0:8000
  fi
}

init_django_project() {
  if bool "$COLLECT_STATIC_FILES"; then
    python3 manage.py collectstatic --noinput
  fi
  python3 manage.py migrate
  python3 manage.py createsuperuser --noinput || true
}

wait_for_postgres
init_django_project

if [ "$1" = "start" ]; then
  run_server
elif [ "$1" = "test" ]; then
  pytest --cov --cov-fail-under=100 -n auto
  bandit .
  flake8 --count
else
  printc "Unknown command: '$1'" "danger"
  printc "Exiting!" "danger"
  exit 1
fi
