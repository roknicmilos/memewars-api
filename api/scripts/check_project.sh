#!/bin/sh

set -e

. /app/scripts/colored_print.sh

printc "\nRunning tests in parallel and checking test coverage...\n" "info"
pytest --cov --cov-fail-under=100 -n auto

printc "\nGenerating html for previously checked test coverage...\n" "info"
coverage html

printc "\nReporting linting issues...\n" "info"
python3 -m flake8 --count

echo
