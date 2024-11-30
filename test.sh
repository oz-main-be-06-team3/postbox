#!/usr/bin/env bash
set -eo pipefail

COLOR_GREEN=`tput setaf 2;`
COLOR_NC=`tput sgr0;` # No Color

# Specify Django settings module
export DJANGO_SETTINGS_MODULE=PostBox.settings.base

echo "Starting black"
poetry run black .
echo "OK"

echo "Starting isort"
poetry run isort .
echo "OK"

echo  "Starting wait_for_db"
poetry run python manage.py wait_for_db
echo  "database is ready"

echo "Starting test with coverage"
poetry run coverage run manage.py test
poetry run coverage report -m

echo "${COLOR_GREEN}All tests passed successfully!${COLOR_NC}"


