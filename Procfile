release: python scripts/setup_heroku.py
web: python nltk_setup.py && gunicorn app:app
worker: python nltk_setup.py && python manage.py rqworker default
