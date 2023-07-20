#!/bin/bash

set -e

cd "$MW_API_STAGING_DIR_PATH"

# Print current location in the file system
# and the content of that location:
echo "Current directory: $PWD"
echo "Content of the current directory:"
ls -la

# Build and start the containers:
docker compose build
docker compose -p memewars-api-staging up -d

# Generate test coverage report that should
# be available on STAGING to view via browser:
docker exec -t memewars-django--staging sh -c 'pytest --create-db --cov -n auto && coverage html'
