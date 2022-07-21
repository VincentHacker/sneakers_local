web: gunicorn sneakers.wsgi
worker: celery -A sneakers worker --beat -l info -S django 