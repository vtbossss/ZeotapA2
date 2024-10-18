from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    main = models.CharField(max_length=50)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    dt = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.main} at {self.fetched_at}"
