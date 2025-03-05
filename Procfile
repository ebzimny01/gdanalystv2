release: python scripts/setup_heroku.py
web: gunicorn gd.wsgi
worker: python manage.py rqworker default
