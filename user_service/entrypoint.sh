#!/bin/sh

cp .env.backup .env 2>/dev/null

python manage.py makemigrations || true
python manage.py migrate || true

python manage.py runserver 0.0.0.0:8000
