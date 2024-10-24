import requests
from datetime import datetime
from django.utils import timezone
from .models import WeatherData, DailyAggregate  # Import models for storing weather data and daily aggregates
from django.conf import settings
from django.db.models import Avg, Max, Min, Count

# API key and a list of metro cities for which weather data is to be fetched
API_KEY = settings.API_KEY
METRO_CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def fetch_weather_data():
    """
    Fetches weather data from OpenWeatherMap for predefined metro cities
    and stores it in the WeatherData model.
    """
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

    # Loop through each metro city and fetch weather data
    for city in METRO_CITIES:
        response = requests.get(url.format(city, API_KEY))
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Convert temperature and "feels like" temperature from Kelvin to Celsius
            temperature = data['main']['temp'] - 273.15
            feels_like = data['main']['feels_like'] - 273.15
            main = data['weather'][0]['main']  # Main weather condition (e.g., Rain, Clear)
            humidity = data['main']['humidity']  # Extract humidity percentage
            wind_speed = data['wind']['speed']  # Extract wind speed in m/s
            dt = datetime.fromtimestamp(data['dt'])  # Convert timestamp to datetime
            dt = timezone.make_aware(dt)  # Make datetime timezone-aware

            # Store the fetched weather data in the database
            WeatherData.objects.create(
                city=city,
                main=main,
                temperature=temperature,
                feels_like=feels_like,
                humidity=humidity,
                wind_speed=wind_speed,
                dt=dt
            )
        else:
            # Log an error if the API request fails
            print(f"Error fetching weather data for {city}: {response.status_code} - {response.text}")

def calculate_daily_aggregates():
    """
    Aggregates daily weather data for the current date, calculating average,
    max, min temperature, humidity, wind speed, and dominant weather condition.
    """
    today = datetime.today().date()

    # Aggregate temperature data, humidity, and wind speed for today
    summary = WeatherData.objects.filter(dt__date=today).aggregate(
        avg_temp=Avg('temperature'),
        max_temp=Max('temperature'),
        min_temp=Min('temperature'),
        avg_humidity=Avg('humidity'),
        max_wind_speed=Max('wind_speed')
    )

    # Determine the most frequent weather condition (dominant weather) for today
    dominant_weather = WeatherData.objects.filter(dt__date=today)\
        .values('main')\
        .annotate(count=Count('main'))\
        .order_by('-count')\
        .first()

    # Set the dominant weather condition, if available
    summary['dominant_weather'] = dominant_weather['main'] if dominant_weather else None

    # Store or update the aggregated data in the DailyAggregate model
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
    return summary

# Thresholds for triggering weather alerts
TEMP_THRESHOLD = 35  # Temperature threshold in Celsius
CONDITION_THRESHOLD = ['Rain', 'Thunderstorm']  # List of weather conditions that trigger alerts

def check_for_alerts(current_temp, weather_condition, city_name):
    """
    Checks if the current temperature or weather condition exceeds predefined thresholds
    and generates appropriate alerts.
    """
    alerts = []
    
    # Check if the temperature exceeds the threshold
    if current_temp > TEMP_THRESHOLD:
        alerts.append(f"Alert for {city_name}: Temperature has exceeded {TEMP_THRESHOLD}°C!")
    
    # Check if the weather condition is in the list of alert-triggering conditions
    if weather_condition in CONDITION_THRESHOLD:
        alerts.append(f"Alert for {city_name}: Weather condition '{weather_condition}' has triggered an alert!")
    
    return alerts
