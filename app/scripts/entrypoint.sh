#!/bin/bash

set -e

. /app/scripts/utils.sh

export REACT_APP_API_URL="$WEB_API_BASE_URL/api/v1"
export REACT_APP_PAGE_SIZE=$DRF_PAGE_SIZE

npm install
if $(bool "$WEB_APP_DEV_SERVER"); then
  printc "Starting development server...\n" "info"
  npm start
else
  printc "Building production ready files and starting production server...\n" "info"
  npm run build
  serve -s build
fi
