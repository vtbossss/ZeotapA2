# weather/urls.py
from django.urls import path
from .views import home, visualizations

app_name = 'weather'

urlpatterns = [
    path('', home, name='home'),
    path('visualizations/', visualizations, name='visualizations'),
]
