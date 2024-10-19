# weather/visualizations.py
import plotly.graph_objects as go
from .models import WeatherData
from django.db.models import Avg
from datetime import datetime, timedelta  # Ensure timedelta is imported


def plot_daily_summary():
    today = datetime.today().date()

    # Fetch daily temperature averages for the current month
    # Fetch daily temperature averages for the last 7 days
    daily_data = WeatherData.objects.filter(fetched_at__date__gte=today - timedelta(days=7)).values('fetched_at__date').annotate(avg_temp=Avg('temperature')).order_by('fetched_at__date')

    # Extract the dates and average temperatures
    dates = [data['fetched_at__date'] for data in daily_data]
    avg_temps = [data['avg_temp'] for data in daily_data]

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=avg_temps, mode='lines+markers', name='Avg Temperature'))

    fig.update_layout(title='Daily Average Temperature',
                      xaxis_title='Date',
                      yaxis_title='Temperature (°C)')

    return fig.to_html(full_html=False)
