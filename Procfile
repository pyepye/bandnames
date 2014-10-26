web: web: python musicify/manage.py collectstatic --noinput --settings=rmusicify.settings.production; gunicorn --pythonpath=./rmusicify rmusicify.wsgi:application
