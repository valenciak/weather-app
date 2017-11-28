from django.conf.urls import url
from forecast.views import WeatherView

urlpatterns = [
    url(r'^$', WeatherView.as_view(), name='forecast')  # default homepage for forecast
]