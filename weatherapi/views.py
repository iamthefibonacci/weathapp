import requests
from django.shortcuts import render

from .forms import WeatherForm
from .models import Weather


def index(request):
    url = 'http://api.weatherapi.com/v1/forecast.json?key=6b8a4fcbb4ac423f9b7195355201311&q={}&days={}'
 
    form = WeatherForm()

    weather_data = []

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        form.save()

        # get the last item inserted into the database
        weather_request = Weather.objects.last()

        r = requests.get(url.format(weather_request.city, weather_request.period)).json()

        city_weather = {
            'city': weather_request.city,
            'icon': r['current']['condition']['icon'],
            'description': r['current']['condition']['text'],
            'temperature': r['current']['temp_c'],
            'humidity': r['current']['humidity'],
            'date': 'Today'
        }
        weather_data.append(city_weather)

        for x in range(0, len(r['forecast']['forecastday'])):
            city_weather = {
                'city': weather_request.city,
                'icon': r['forecast']['forecastday'][x]['day']['condition']['icon'],
                'description': r['forecast']['forecastday'][x]['day']['condition']['text'],
                'date': r['forecast']['forecastday'][x]['date'],
                'average_temp': r['forecast']['forecastday'][x]['day']['avgtemp_c'],
                'max_temp': r['forecast']['forecastday'][x]['day']['maxtemp_c'],
                'min_temp': r['forecast']['forecastday'][x]['day']['mintemp_c'],
                'median_temp': round((r['forecast']['forecastday'][x]['day']['mintemp_c'] +
                                      r['forecast']['forecastday'][x]['day']['maxtemp_c']) / 2, 1),
                'humidity': r['forecast']['forecastday'][x]['hour'][0]['humidity'],
            }
            weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)
