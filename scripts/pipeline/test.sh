#!/bin/bash

set -e

# Print current location in the file system
# and the content of that location:
echo "Current directory: $PWD"
echo "Content of the current directory:"
ls -la

# Build the necessary images with default environment variables:
cp example.env .env
docker compose -f docker-compose.test.yml build --no-cache

# Make sure there are no containers from previous runs:
docker compose -f docker-compose.test.yml down

# Run "django" container that runs tests and checks:
docker compose -f docker-compose.test.yml run --rm django

# Make sure to remove all started containers:
docker compose -f docker-compose.test.yml down
