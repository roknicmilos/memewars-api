#!/bin/bash

set -e

cd "$MW_API_PRODUCTION_DIR_PATH"

# Print current location in the file system
# and the content of that location:
echo "Current directory: $PWD"
echo "Content of the current directory:"
ls -la

# Checkout to the latest "main" branch version:
git fetch origin
git checkout -B main origin/main || exit

# Build and start the containers:
docker compose build
docker compose -p memewars-api-production up -d
