from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    main = models.CharField(max_length=50)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.IntegerField(default=50)  # New field with default 50%
    wind_speed = models.FloatField(default=0)  # New field with default 0 m/s
    dt = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"

from django.utils import timezone

class DailyAggregate(models.Model):
    # Field to store the date of the aggregate
    date = models.DateField(default=timezone.now, unique=True)

    # Fields to store aggregated data
    avg_temp = models.FloatField(null=True, blank=True)
    max_temp = models.FloatField(null=True, blank=True)
    min_temp = models.FloatField(null=True, blank=True)
    avg_humidity = models.FloatField(null=True, blank=True)
    max_wind_speed = models.FloatField(null=True, blank=True)

    # Field to store the dominant weather condition
    dominant_weather = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Daily Aggregate for {self.date}"
