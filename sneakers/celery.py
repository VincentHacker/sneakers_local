import os

from celery import Celery
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sneakers.settings')

app = Celery('sneakers')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(result_expires=3600, enable_utc=True, timezone='UTC')
app.conf.beat_schedule = {}
app.conf.timezone = 'UTC'