# weather/views.py
from django.shortcuts import render
from .models import WeatherData
from .utils import calculate_daily_aggregates
from django.db.models import OuterRef, Subquery
from django.db.models import Max
from .utils import calculate_daily_aggregates, check_for_alerts


    
def home(request):
    # Get the latest weather data for each city
    latest_dates = WeatherData.objects.values('city').annotate(latest_fetched_at=Max('fetched_at'))
    
    # Use the latest dates to filter the most recent data for each city
    latest_data = WeatherData.objects.filter(
        city__in=[item['city'] for item in latest_dates],
        fetched_at__in=[item['latest_fetched_at'] for item in latest_dates]
    )
    
    daily_summary = calculate_daily_aggregates()
    
    # Get the first city's weather data for alert (you can customize this for all cities)
    alerts = []
    for city_weather in latest_data:
        temperature = city_weather.temperature
        weather_condition = city_weather.main
        
        # Check if any alerts are triggered for each city
        city_alerts = check_for_alerts(temperature, weather_condition)
        if city_alerts:
            alerts.extend(city_alerts)


    return render(request, 'home.html', {
        'latest_data': latest_data,
        'daily_summary': daily_summary,
        'alerts': alerts,  # Pass the alerts to the template
    })


# weather/views.py
from .visualizations import plot_daily_summary
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def visualizations(request):
    plot_html = plot_daily_summary()  # Get the plot HTML
    return render(request, 'visualizations.html', {'plot_html': plot_html})

