from django.urls import path
from weatherapp.views import weather_view
urlpatterns = [
    path('', weather_view, name='weather_view'),
]