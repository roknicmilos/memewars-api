#!/bin/sh

set -e

export REACT_APP_API_URL=$API_URL

npm install
npm start
