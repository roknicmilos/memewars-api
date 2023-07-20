#!/bin/bash

set -e

# Print current location in the file system
# and the content of that location:
echo "Current directory: $PWD"
echo "Content of the current directory:"
ls -la

# Build and start the necessary containers that
# will run tests, and clean them afterwards:
cp example.env .env
docker compose -f docker-compose.test.yml build --no-cache
docker compose -f docker-compose.test.yml run --rm django
docker compose down
