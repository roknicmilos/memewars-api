#!/bin/bash

set -e

echo "MW_API_STAGING_DIR_PATH: $MW_API_STAGING_DIR_PATH"
cd "$MW_API_STAGING_DIR_PATH"
echo "Current directory: $PWD"
echo "Content of the current directory:"
ls -la
echo "Content of .env file:"
cat .env
