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
