# weather/alerts.py
from .models import WeatherData  # Import the WeatherData model

def check_thresholds():
    latest_data = WeatherData.objects.latest('fetched_at')
    if latest_data.temperature > 35:
        print(f"ALERT! Temperature exceeded 35°C in {latest_data.city}")
