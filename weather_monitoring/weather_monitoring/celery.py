from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_monitoring.settings')

app = Celery('weather_monitoring')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'calculate-daily-aggregates': {
        'task': 'weather.tasks.daily_aggregate_task',
        'schedule': crontab(hour=23, minute=59),  # Runs every day at 11:59 PM
    },
}
