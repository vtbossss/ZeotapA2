from django.shortcuts import render
from .models import WeatherData
from .utils import calculate_daily_aggregates, check_for_alerts
from django.db.models import Max
from django.http import StreamingHttpResponse
import json
import time

# View for rendering the home page with weather data and daily summaries
def home(request):
    """
    Renders the home page with the latest weather data for each city,
    daily summary, and any triggered alerts.
    """
    
    # Get the latest weather data for each city by fetching the most recent 'fetched_at' timestamp
    latest_dates = WeatherData.objects.values('city').annotate(latest_fetched_at=Max('fetched_at'))
    
    # Filter the most recent weather data for each city using the latest fetched dates
    latest_data = WeatherData.objects.filter(
        city__in=[item['city'] for item in latest_dates],
        fetched_at__in=[item['latest_fetched_at'] for item in latest_dates]
    )

    # Calculate the daily weather summary
    daily_summary = calculate_daily_aggregates()
    alerts = []

    # Check for alerts based on temperature and weather conditions for each city
    for city_weather in latest_data:
        temperature = city_weather.temperature
        weather_condition = city_weather.main
        city_name = city_weather.city

        # Generate alerts for the city, if any
        city_alerts = check_for_alerts(temperature, weather_condition, city_name)
        if city_alerts:
            alerts.extend(city_alerts)

    # Render the home page template with the latest weather data, daily summary, and alerts
    return render(request, 'home.html', {
        'latest_data': latest_data,  # Pass the latest weather data including humidity and wind speed
        'daily_summary': daily_summary,
        'alerts': alerts,
    })

# Streaming the weather data using Server-Sent Events (SSE)
def stream_weather_data(request):
    """
    Streams the latest weather data to the client using Server-Sent Events (SSE).
    Sends updates every 30 seconds.
    """
    def event_stream():
        while True:
            # Fetch the latest weather data for each city
            latest_dates = WeatherData.objects.values('city').annotate(latest_fetched_at=Max('fetched_at'))
            latest_data = WeatherData.objects.filter(
                city__in=[item['city'] for item in latest_dates],
                fetched_at__in=[item['latest_fetched_at'] for item in latest_dates]
            )

            # Prepare the weather data as a list of dictionaries, including humidity and wind speed
            data = [
                {
                    "city": weather.city,
                    "temperature": weather.temperature,
                    "feels_like": weather.feels_like,
                    "main": weather.main,
                    "humidity": weather.humidity,  # Added humidity data
                    "wind_speed": weather.wind_speed,  # Added wind speed data
                    "fetched_at": weather.fetched_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for weather in latest_data
            ]

            # Send the data as a Server-Sent Event (SSE) using json.dumps to convert it to JSON
            yield f"data: {json.dumps(data)}\n\n"

            time.sleep(30)  # Wait for 30 seconds before sending the next update

    # Return the streaming response with the event stream
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

# View for displaying visualizations
from .visualizations import plot_daily_summary

def visualizations(request):
    """
    Renders the visualizations page with a Plotly chart for the daily weather summary.
    """
    plot_html = plot_daily_summary()  # Get the plot HTML for visualizations
    return render(request, 'visualizations.html', {'plot_html': plot_html})

# Another version of event stream for weather data (not used currently)
def sse_weather_data(request):
    """
    Alternative version of streaming weather data using SSE.
    Sends updates every 5 seconds.
    """
    def event_stream():
        while True:
            # Fetch the latest weather data for each city
            latest_dates = WeatherData.objects.values('city').annotate(latest_fetched_at=Max('fetched_at'))
            latest_data = WeatherData.objects.filter(
                city__in=[item['city'] for item in latest_dates],
                fetched_at__in=[item['latest_fetched_at'] for item in latest_dates]
            )
            
            # Prepare the data for SSE, including a timestamp
            data = {
                'latest_data': list(latest_data.values()),  # Convert queryset to a list of values
                'timestamp': time.time()  # Add a timestamp for the client
            }
            
            yield f"data: {data}\n\n"
            time.sleep(5)  # Send updates every 5 seconds

    # Return the streaming response for SSE
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'  # Ensure that the response is not cached
    return response
