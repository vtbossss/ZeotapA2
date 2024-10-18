import matplotlib.pyplot as plt
from .models import WeatherData
from datetime import datetime

def plot_daily_summary():
    today = datetime.today().date()
    data = WeatherData.objects.filter(fetched_at__date=today).values_list('temperature', flat=True)
    plt.plot(data)
    plt.title("Daily Temperature Trend")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.show()
