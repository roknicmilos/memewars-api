#!/bin/sh

set -e

. /app/scripts/colored_print.sh

wait_for_postgres() {
  # Adapted from https://docs.docker.com/compose/startup-order/
  echo 'Waiting for PostgreSQL...'
  until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOSTNAME" -U "$DB_USERNAME" -d "$DB_NAME" -c '\q'; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
  done
}

print_django_project_init_info() {
  printc "Starting Django app in $ENVIRONMENT mode \n" "info"
  printc "WEB API base URL: $WEB_API_BASE_URL \n" "info"
  printc "WEB APP base URL: $WEB_APP_BASE_URL \n" "info"
}

init_django_project() {
  if [ "$ENVIRONMENT" = 'development' ]; then
    print_django_project_init_info
    python3 manage.py migrate
    python3 manage.py create_superuser --noinput
    python3 manage.py runserver 0.0.0.0:8000

  elif [ "$ENVIRONMENT" = 'production' ]; then
    print_django_project_init_info
    python3 manage.py collectstatic --noinput
    python3 manage.py migrate
    gunicorn meme_wars.wsgi --bind 0.0.0.0:8000

  else
    printc "[ERROR]: Unknown environment: '$ENVIRONMENT'\n" "danger"
    printc "Exiting... \n\n"
    exit 1
  fi
}

wait_for_postgres
init_django_project
