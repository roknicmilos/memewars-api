#!/bin/bash

set -e

# Print current location in the file system
# and the content of that location:
echo "Current directory: $PWD"
echo "Content of the current directory:"
sh "ls -la"

# Build and start the necessary containers that
# will run tests, and clean them afterwards:
sh "cp example.env .env"
sh "docker compose -f docker-compose.test.yml build --no-cache"
sh "docker compose -f docker-compose.test.yml run --rm django"
sh "docker compose down"
