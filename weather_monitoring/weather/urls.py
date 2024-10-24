from django.urls import path
from .views import home, visualizations, stream_weather_data

app_name = 'weather'

urlpatterns = [
    path('', home, name='home'),  # Home page route
    path('visualizations/', visualizations, name='visualizations'),  # Visualizations page route
    path('stream_weather/', stream_weather_data, name='stream_weather'),  # New endpoint for streaming weather data
]
