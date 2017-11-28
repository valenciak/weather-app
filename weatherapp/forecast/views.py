from django.views.generic import View
from django.shortcuts import render
from forecast.forms import InputForm
from forecast.models import Weather, Weekdays, Future
import googlemaps
from forecastiopy import *
from datetime import datetime, timedelta
from weatherapp.settings import GOOGLE_API_KEY, DARKSKY_API_KEY


class WeatherView(View):
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    weekdays_default = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    template_name = 'forecast/results.html'

    def get(self, request):
        form = InputForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        weather = Weather()
        future = Future()
        gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
        form = InputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            geocode_result = gmaps.geocode(text)
            self.assign_weather_attr(weather, future, geocode_result)
            form = InputForm()
        return render(request, self.template_name, {'form': form, 'weather': weather, 'future': future})

    def assign_weather_attr(self, weather, future, geocode_result):
        weekdays_current = Weekdays()
        current = self.forecast(geocode_result)[0]
        hourly = self.forecast(geocode_result)[1]
        daily = self.forecast(geocode_result)[2]
        weather.summary = hourly.summary
        weather.timestamp = current.time
        weather.temperature = int(current.temperature)
        weather.location = self.location(geocode_result)
        weather.precipitation = current.precipProbability
        weather.date = self.date(current)
        weekday_int = datetime.today().weekday() % 7
        self.weekdays(weekdays_current, weekday_int)
        weather.weekdays = weekdays_current
        weather.wind_speed = current.windSpeed
        weather.icon = current.icon

        future.two.low = int(daily.get_day(2)['temperatureLow'])
        future.two.high = int(daily.get_day(2)['temperatureHigh'])
        future.two.icon = daily.get_day(2)['icon']

        future.three.low = int(daily.get_day(3)['temperatureLow'])
        future.three.high = int(daily.get_day(3)['temperatureHigh'])
        future.three.icon = daily.get_day(3)['icon']

        future.four.low = int(daily.get_day(4)['temperatureLow'])
        future.four.high = int(daily.get_day(4)['temperatureHigh'])
        future.four.icon = daily.get_day(4)['icon']

        future.five.low = int(daily.get_day(5)['temperatureLow'])
        future.five.high = int(daily.get_day(5)['temperatureHigh'])
        future.five.icon = daily.get_day(5)['icon']

        future.six.low = int(daily.get_day(6)['temperatureLow'])
        future.six.high = int(daily.get_day(6)['temperatureHigh'])
        future.six.icon = daily.get_day(6)['icon']

        future.seven.low = int(daily.get_day(7)['temperatureLow'])
        future.seven.high = int(daily.get_day(7)['temperatureHigh'])
        future.seven.icon = daily.get_day(7)['icon']

    @staticmethod
    def forecast(geocode_result):
        lat = geocode_result[0]['geometry']['location']['lat']
        long = geocode_result[0]['geometry']['location']['lng']
        fio = ForecastIO.ForecastIO(DARKSKY_API_KEY, units=ForecastIO.ForecastIO.UNITS_US, latitude=lat, longitude=long)
        return [FIOCurrently.FIOCurrently(fio), FIOHourly.FIOHourly(fio), FIODaily.FIODaily(fio)]

    @staticmethod
    def location(geocode_result):
        city = str(geocode_result[0]['address_components'][1]['long_name']) if \
            geocode_result[0]['address_components'][0]['types'] == ["postal_code"] else \
            str(geocode_result[0]['address_components'][0]['long_name'])
        state = str(geocode_result[0]['address_components'][-2]['short_name'])
        return city + ", " + state

    @staticmethod
    def date(current):
        day = datetime.fromtimestamp(
            int(current.time)
        ).strftime('%d')
        month = WeatherView.months[int(datetime.fromtimestamp(
            int(current.time)
        ).strftime('%m'))]
        return day + ' ' + month

    @staticmethod
    def weekdays(weekdays, weekday_int):
        weekdays.one = WeatherView.weekdays_default[weekday_int]
        weekdays.two = WeatherView.weekdays_default[(weekday_int+1) % 7]
        weekdays.three = WeatherView.weekdays_default[(weekday_int+2) % 7]
        weekdays.four = WeatherView.weekdays_default[(weekday_int+3) % 7]
        weekdays.five = WeatherView.weekdays_default[(weekday_int+4) % 7]
        weekdays.six = WeatherView.weekdays_default[(weekday_int+5) % 7]
        weekdays.seven = WeatherView.weekdays_default[(weekday_int+6) % 7]

