from celery import shared_task
from .utils import fetch_weather_data, calculate_daily_aggregates  # Import required utilities
from .alerts import check_thresholds  # Import alerts for threshold checks


# Task to periodically update weather data
@shared_task
def periodic_weather_update():
    fetch_weather_data()
    check_thresholds()


# Task to calculate daily aggregates
@shared_task
def daily_aggregate_task():
    calculate_daily_aggregates()
