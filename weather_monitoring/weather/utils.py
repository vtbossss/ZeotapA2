# weather/utils.py

import requests
from datetime import datetime
from django.utils import timezone
from .models import WeatherData # Ensure your WeatherData model is imported
from django.conf import settings

API_KEY = settings.API_KEY
METRO_CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def fetch_weather_data():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    for city in METRO_CITIES:
        response = requests.get(url.format(city, API_KEY))
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
            feels_like = data['main']['feels_like'] - 273.15
            main = data['weather'][0]['main']
            dt = datetime.fromtimestamp(data['dt'])
            dt = timezone.make_aware(dt)  # Make datetime timezone-aware

            # Store data in the database
            WeatherData.objects.create(
                city=city,
                main=main,
                temperature=temperature,
                feels_like=feels_like,
                dt=dt  # Use the timezone-aware datetime
            )
        else:
            print(f"Error fetching weather data for {city}: {response.status_code} - {response.text}")
from django.db.models import Avg, Max, Min, Count


def calculate_daily_aggregates():
    today = datetime.today().date()
    
    # Aggregate temperature data
    summary = WeatherData.objects.filter(fetched_at__date=today).aggregate(
        avg_temp=Avg('temperature'),
        max_temp=Max('temperature'),
        min_temp=Min('temperature'),
    )
    
    # Get the dominant weather condition separately
    dominant_weather = WeatherData.objects.filter(fetched_at__date=today)\
        .values('main')\
        .annotate(count=Count('main'))\
        .order_by('-count')\
        .first()
    
    summary['dominant_weather'] = dominant_weather['main'] if dominant_weather else None
    return summary
