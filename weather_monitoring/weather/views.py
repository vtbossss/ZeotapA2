from django.shortcuts import render
from .models import WeatherData
from .utils import calculate_daily_aggregates, check_for_alerts
from django.db.models import Max
from django.http import StreamingHttpResponse
import json
import time

# View for rendering the home page with weather data and daily summaries
def home(request):
    # Get the latest weather data for each city
    latest_dates = WeatherData.objects.values('city').annotate(latest_fetched_at=Max('fetched_at'))
    
    # Use the latest dates to filter the most recent data for each city
    latest_data = WeatherData.objects.filter(
        city__in=[item['city'] for item in latest_dates],
        fetched_at__in=[item['latest_fetched_at'] for item in latest_dates]
    )

    # Fetch daily summary and alerts
    daily_summary = calculate_daily_aggregates()
    alerts = []

    # Check for alerts for each city's weather data
    for city_weather in latest_data:
        temperature = city_weather.temperature
        weather_condition = city_weather.main
        city_name = city_weather.city

        # Check if any alerts are triggered for each city
        city_alerts = check_for_alerts(temperature, weather_condition, city_name)
        if city_alerts:
            alerts.extend(city_alerts)

    # Render the template with weather data, daily summary, and alerts
    return render(request, 'home.html', {
        'latest_data': latest_data,  # Pass latest weather data including humidity and wind speed
        'daily_summary': daily_summary,
        'alerts': alerts,
    })

# Streaming the weather data using Server-Sent Events (SSE)
def stream_weather_data(request):
    def event_stream():
        while True:
            # Fetch the latest weather data
            latest_dates = WeatherData.objects.values('city').annotate(latest_fetched_at=Max('fetched_at'))
            latest_data = WeatherData.objects.filter(
                city__in=[item['city'] for item in latest_dates],
                fetched_at__in=([item['latest_fetched_at'] for item in latest_dates])
            )

            # Prepare the data as a list of dictionaries, including humidity and wind speed
            data = [
                {
                    "city": weather.city,
                    "temperature": weather.temperature,
                    "feels_like": weather.feels_like,
                    "main": weather.main,
                    "humidity": weather.humidity,  # Added humidity
                    "wind_speed": weather.wind_speed,  # Added wind speed
                    "fetched_at": weather.fetched_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for weather in latest_data
            ]

            # Send the data as SSE using json.dumps to convert to JSON
            yield f"data: {json.dumps(data)}\n\n"

            time.sleep(30)  # Wait for 30 seconds before sending the next update

    # Return the streaming response
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

# View for displaying visualizations
from .visualizations import plot_daily_summary
def visualizations(request):
    plot_html = plot_daily_summary()  # Get the plot HTML
    return render(request, 'visualizations.html', {'plot_html': plot_html})

# Another version of event stream for weather data (not used currently)
def sse_weather_data(request):
    def event_stream():
        while True:
            latest_dates = WeatherData.objects.values('city').annotate(latest_fetched_at=Max('fetched_at'))
            latest_data = WeatherData.objects.filter(
                city__in=([item['city'] for item in latest_dates]),
                fetched_at__in=([item['latest_fetched_at'] for item in latest_dates])
            )
            
            # Prepare the data for SSE
            data = {
                'latest_data': list(latest_data.values()),
                'timestamp': time.time()  # Optional timestamp for the client
            }
            
            yield f"data: {data}\n\n"
            time.sleep(5)  # Adjust the frequency of updates as needed

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
