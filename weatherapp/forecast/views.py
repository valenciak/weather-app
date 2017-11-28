from django.views.generic import View
from django.shortcuts import render, redirect
from forecast.forms import InputForm
import googlemaps
from forecastiopy import *
import datetime
from weatherapp.settings import GOOGLE_API_KEY, DARKSKY_API_KEY


class WeatherView(View):
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    template_name = 'forecast/results.html'

    # def results(self, request):
    #     form = InputForm(request.POST)
    #     if form.is_valid():
    #         text = form.cleaned_data['post']
    #         print("hi")
    #         print(text)
    #     args = {'form': form, 'text': text}
    #     return render(request, self.template_name, args)

    def get(self, request):
        form = InputForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
        form = InputForm(request.POST)
        args = {}
        if form.is_valid():
            text = form.cleaned_data['post']
            geocode_result = gmaps.geocode(text)
            city = str(geocode_result[0]['address_components'][1]['long_name']) if \
                geocode_result[0]['address_components'][0]['types'] == [ "postal_code" ] else \
                str(geocode_result[0]['address_components'][0]['long_name'])
            state = str(geocode_result[0]['address_components'][-2]['short_name'])
            location_name = city + ", " + state
            print(location_name)
            lat = geocode_result[0]['geometry']['location']['lat']
            long = geocode_result[0]['geometry']['location']['lng']
            fio = ForecastIO.ForecastIO(DARKSKY_API_KEY, units=ForecastIO.ForecastIO.UNITS_US, latitude=lat, longitude=long)
            current = FIOCurrently.FIOCurrently(fio)
            print(geocode_result)
            args['precipitation'] = current.precipProbability
            day = datetime.datetime.fromtimestamp(
                int(current.time)
                ).strftime('%d')
            month = self.months[int(datetime.datetime.fromtimestamp(
                int(current.time)
                ).strftime('%m'))]
            args['date'] = day + ' ' + month
            args['temp'] = int(current.temperature)
            args['location'] = location_name
            args['wind_speed'] = current.windSpeed
            args['icon'] = current.icon
            print(current.icon)
            form = InputForm()
        args['form'] = form
        print("Args: ", args)
        return render(request, self.template_name, args)

