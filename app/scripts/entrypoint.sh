#!/bin/sh

set -e

. /app/scripts/colored_print.sh

export REACT_APP_API_URL="$WEB_API_BASE_URL:$WEB_API_PORT/api/v1"

print_react_project_init_info() {
  printc "Starting React app in $ENVIRONMENT mode \n" "info"
  printc "WEB API URL: $REACT_APP_API_URL\n" "info"
}

init_react_project() {
  if [ "$ENVIRONMENT" = 'development' ]; then
    print_react_project_init_info
    npm install
    npm start

  elif [ "$ENVIRONMENT" = 'production' ] || [ "$ENVIRONMENT" = 'staging' ]; then
    print_react_project_init_info
    npm install
    npm run build
    serve -s build

  else
    printc "[ERROR]: Unknown React app environment: '$ENVIRONMENT'\n" "danger"
    printc "Exiting... \n\n"
    exit 1
  fi
}

init_react_project
