#!/bin/bash

set -e

cd "$MW_API_STAGING_DIR_PATH"

echo "Current directory: $PWD"

echo "Content of the current directory:"
ls -la

docker compose build
docker compose -p memewars-api-staging up -d
docker exec -t memewars-django--staging sh -c 'pytest --create-db --cov -n auto && coverage html'
