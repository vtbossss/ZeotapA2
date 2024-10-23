import requests
from datetime import datetime
from django.utils import timezone
from .models import WeatherData,DailyAggregate  # Ensure your WeatherData model is imported
from django.conf import settings
from django.db.models import Avg, Max, Min, Count

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
            humidity = data['main']['humidity']  # Extract humidity
            wind_speed = data['wind']['speed']  # Extract wind speed
            dt = datetime.fromtimestamp(data['dt'])
            dt = timezone.make_aware(dt)  # Make datetime timezone-aware

            # Store data in the database
            WeatherData.objects.create(
                city=city,
                main=main,
                temperature=temperature,
                feels_like=feels_like,
                humidity=humidity,  # Store humidity
                wind_speed=wind_speed,  # Store wind speed
                dt=dt  # Use the timezone-aware datetime
            )
        else:
            print(f"Error fetching weather data for {city}: {response.status_code} - {response.text}")

def calculate_daily_aggregates():
    today = datetime.today().date()
    
    # Aggregate temperature data along with humidity and wind speed
    summary = WeatherData.objects.filter(dt__date=today).aggregate(
        avg_temp=Avg('temperature'),
        max_temp=Max('temperature'),
        min_temp=Min('temperature'),
        avg_humidity=Avg('humidity'),  # Aggregate humidity
        max_wind_speed=Max('wind_speed')  # Aggregate wind speed
    )
    
    # Get the dominant weather condition separately
    dominant_weather = WeatherData.objects.filter(dt__date=today)\
        .values('main')\
        .annotate(count=Count('main'))\
        .order_by('-count')\
        .first()
    
    summary['dominant_weather'] = dominant_weather['main'] if dominant_weather else None
    
    # Store the summary in DailyAggregate model
    DailyAggregate.objects.update_or_create(
        date=today,
        defaults={
            'avg_temp': summary['avg_temp'],
            'max_temp': summary['max_temp'],
            'min_temp': summary['min_temp'],
            'avg_humidity': summary['avg_humidity'],
            'max_wind_speed': summary['max_wind_speed'],
            'dominant_weather': summary['dominant_weather']
        }
    )

# Hard-coded threshold values
TEMP_THRESHOLD = 35  # degrees Celsius
CONDITION_THRESHOLD = ['Rain', 'Thunderstorm']  # Weather conditions that trigger alerts

def check_for_alerts(current_temp, weather_condition, city_name):
    """Check if the temperature or weather condition exceeds defined thresholds."""
    alerts = []
    
    # Check for temperature breach
    if current_temp > TEMP_THRESHOLD:
        alerts.append(f"Alert for {city_name}: Temperature has exceeded {TEMP_THRESHOLD}°C!")
    
    # Check for weather condition breach
    if weather_condition in CONDITION_THRESHOLD:
        alerts.append(f"Alert for {city_name}: Weather condition '{weather_condition}' has triggered an alert!")
    
    return alerts
