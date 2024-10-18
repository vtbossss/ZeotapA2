import requests
from datetime import datetime
from .models import WeatherData

API_KEY = '9bd1f33be3923e9ef3e78fc5068ed68f'
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

            # Store data in the database
            WeatherData.objects.create(
                city=city,
                main=main,
                temperature=temperature,
                feels_like=feels_like,
                dt=dt
            )
        else:
            print(f"Error fetching weather data for {city}: {response.status_code} - {response.text}")
