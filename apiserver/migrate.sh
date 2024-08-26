#!/bin/bash

cd /app/

echo "start migrate database"

/opt/venv/bin/python manage.py migrate

echo "end migrate database"