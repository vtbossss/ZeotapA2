# weather/visualizations.py
import plotly.graph_objects as go  # Import Plotly for visualization
from .models import WeatherData  # Import WeatherData model for querying data
from django.db.models import Avg  # Import Avg for calculating average values
from datetime import datetime, timedelta  # Import datetime and timedelta for date manipulation

def plot_daily_summary():
    # Get today's date
    today = datetime.today().date()

    # Fetch daily temperature averages for the last 7 days
    daily_data = WeatherData.objects.filter(
        fetched_at__date__gte=today - timedelta(days=7)
    ).values('fetched_at__date').annotate(
        avg_temp=Avg('temperature')
    ).order_by('fetched_at__date')

    # Extract the dates and average temperatures from the fetched data
    dates = [data['fetched_at__date'] for data in daily_data]
    avg_temps = [data['avg_temp'] for data in daily_data]

    # Create a Plotly figure for visualization
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=avg_temps, 
        mode='lines+markers', 
        name='Avg Temperature'  # Name of the trace
    ))

    # Update the layout of the figure
    fig.update_layout(
        title='Daily Average Temperature',  # Title of the plot
        xaxis_title='Date',  # Label for the x-axis
        yaxis_title='Temperature (°C)'  # Label for the y-axis
    )

    # Return the HTML representation of the figure
    return fig.to_html(full_html=False)
