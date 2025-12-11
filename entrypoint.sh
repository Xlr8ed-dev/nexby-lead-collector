#!/bin/sh

# Collect static files
python manage.py collectstatic --noinput

# Ensure log directory exists and is writable
mkdir -p /usr/src/app/logs
chmod -R 777 /usr/src/app/logs

# Run Gunicorn with exec to replace the shell process
exec gunicorn leadcollector.wsgi:application \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    --log-level debug \
    --access-logfile - \
    --error-logfile - \
    --capture-output
