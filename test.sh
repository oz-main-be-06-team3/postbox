#!/usr/bin/env bash
set -eo pipefail

COLOR_GREEN=`tput setaf 2;`
COLOR_NC=`tput sgr0;` # No Color

echo "=============================="
echo "Django 프로젝트 테스트 시작"
echo "=============================="

# 가상환경 활성화
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
else
  echo "에러: 가상환경(.venv)이 존재하지 않습니다. 가상환경을 생성한 후 다시 시도하세요."
  exit 1
fi
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


