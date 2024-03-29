#!/bin/bash

set -e

. /app/scripts/utils.sh

wait_for_postgres() {
  # Adapted from https://docs.docker.com/compose/startup-order/
  printc "Waiting for PostgreSQL...\n" "info"
  until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOSTNAME" -U "$DB_USERNAME" -d "$DB_NAME" -c '\q'; do
    printc >&2 "Postgres is unavailable - sleeping\n" "info"
    sleep 1
  done
}

init_django_project() {
  if bool "$COLLECT_STATIC_FILES"; then
    python3 manage.py collectstatic --noinput
  fi
  python3 manage.py migrate
  python3 manage.py createsuperuser --noinput || true
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

fail_isort() {
  printc "Issues found by 'isort'! " "danger"
  printc "Check the output above to locate and fix the issues\n" "danger"
  exit 1
}

run_checks() {
  # Runs multiple lingers and formatters to check if there are any issues.
  # It doesn't modify the code, it just reports the issues and necessary actions.

  printc "[bandit] Checking code security issues...\n" "info"
  bandit .
  printc "[flake8] Checking linting issues...\n" "info"
  flake8 --toml-config=pyproject.toml .
  printc "[black] Checking formatting issues...\n" "info"
  black --check .
  printc "[isort] Checking issues with import...\n" "info"
  isort --check . && printc "No issues with imports.\n" "success" || fail_isort
}

if [ "$1" = "start" ]; then
  wait_for_postgres
  init_django_project
  run_server

elif [ "$1" = "test" ]; then
  printc "Running tests (pytest) with expected 100% coverage...\n" "info"
  pytest --cov --cov-report term:skip-covered --cov-fail-under=100 -n auto
  run_checks

elif [ "$1" = "check" ]; then
  run_checks

else
  printc "Unknown command: '$1'\n" "danger"
  printc "Exiting!\n" "danger"
  exit 1
fi
