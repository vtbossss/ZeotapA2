from celery import shared_task
from .utils import fetch_weather_data

@shared_task
def periodic_weather_update():
    fetch_weather_data()
