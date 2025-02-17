#!/usr/bin/env bash
# Exit on error
#set -o errexit

make install

#poetry run python manage.py collectstatic --no-input

#poetry run python manage.py migrate