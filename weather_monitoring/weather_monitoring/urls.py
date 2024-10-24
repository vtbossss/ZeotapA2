from django.contrib import admin  # Import the admin module for admin site
from django.urls import path, include  # Import path and include for URL routing

# URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('', include('weather.urls')),  # Include URLs from the 'weather' app
]
