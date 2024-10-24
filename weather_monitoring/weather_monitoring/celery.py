from __future__ import absolute_import  # Ensure compatibility with Python 2 and 3
import os  # Import os for environment variable management
from celery import Celery  # Import Celery for task management
from celery.schedules import crontab  # Import crontab for scheduling tasks

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_monitoring.settings')

# Create a new Celery application instance
app = Celery('weather_monitoring')

# Load configuration from Django settings, using the 'CELERY' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed Django apps
app.autodiscover_tasks()

# Define the Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'calculate-daily-aggregates': {
        'task': 'weather.tasks.daily_aggregate_task',  # Specify the task to run
        'schedule': crontab(hour=23, minute=59),  # Schedule to run daily at 11:59 PM
    },
}
