web: web: python bandnames/manage.py collectstatic --noinput --settings=bandnames.settings.production --pythonpath=/app/bandnames; gunicorn --pythonpath=/app/bandnames bandnames.wsgi:application
