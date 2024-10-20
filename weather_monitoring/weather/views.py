from django.shortcuts import render
from .models import WeatherData
from .utils import calculate_daily_aggregates, check_for_alerts
from django.db.models import Max

def home(request):
    # Get the latest weather data for each city
    latest_dates = WeatherData.objects.values('city').annotate(latest_fetched_at=Max('fetched_at'))
    
    # Use the latest dates to filter the most recent data for each city
    latest_data = WeatherData.objects.filter(
        city__in=[item['city'] for item in latest_dates],
        fetched_at__in=[item['latest_fetched_at'] for item in latest_dates]
    )
    
    daily_summary = calculate_daily_aggregates()
    
    # Initialize alerts list
    alerts = []

    # Check alerts for each city's weather data
    for city_weather in latest_data:
        temperature = city_weather.temperature
        weather_condition = city_weather.main
        city_name = city_weather.city  # Get the city name

        # Check if any alerts are triggered for each city
        city_alerts = check_for_alerts(temperature, weather_condition, city_name)  # Pass city name
        if city_alerts:
            alerts.extend(city_alerts)

    return render(request, 'home.html', {
        'latest_data': latest_data,
        'daily_summary': daily_summary,
        'alerts': alerts,  # Pass the alerts to the template
    })

from .visualizations import plot_daily_summary
# Keep the visualizations function unchanged if no modifications are required there
def visualizations(request):
    plot_html = plot_daily_summary()  # Get the plot HTML
    return render(request, 'visualizations.html', {'plot_html': plot_html})
