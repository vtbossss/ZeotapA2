from celery import shared_task
from .utils import fetch_weather_data




from .alerts import check_thresholds

@shared_task
def periodic_weather_update():
    fetch_weather_data()
    check_thresholds()

from .utils import calculate_daily_aggregates  # Ensure the function is correctly imported

@shared_task
def daily_aggregate_task():
    calculate_daily_aggregates()