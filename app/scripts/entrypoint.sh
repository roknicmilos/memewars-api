#!/bin/sh

set -e

export REACT_APP_API_URL="$WEB_API_BASE_URL/api/v1"

npm install
npm start
