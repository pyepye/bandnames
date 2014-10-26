web: web: python bandnames/manage.py collectstatic --noinput --settings=bandnames.settings.production --pythonpath=./band-names/bandnames; gunicorn --pythonpath=./bandnames bandnames.wsgi:application
