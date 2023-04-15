#!/bin/sh

set -e

. /app/scripts/colored_print.sh

printc "\nRunning tests in parallel and checking test coverage...\n" "info"
pytest --cov -n auto

printc "\nGenerating html for previously checked test coverage...\n" "info"
coverage html

printc "\nChecking security of the code...\n" "info"
bandit .

printc "\nReporting linting issues...\n" "info"
flake8 --count


echo
