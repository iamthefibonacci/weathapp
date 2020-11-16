import requests
from django.shortcuts import render

from .forms import WeatherForm
from .models import Weather


def index(request):
    url = 'http://api.weatherapi.com/v1/forecast.json?key=6b8a4fcbb4ac423f9b7195355201311&q={}&days={}'
    # api.openweathermap.org/data/2.5/forecast/daily?q=london&cnt=7&appid=c2a062459fc88416e6f4ecdac9217cb0
    # http://api.openweathermap.org/data/2.5/weather?q={}&appid=c2a062459fc88416e6f4ecdac9217cb0

    form = WeatherForm()

    weather_data = []

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        form.save()

        # print(form.city)
        # print(form.period)

        # get the last item inserted into the database
        weather_request = Weather.objects.last()

        # for w_request in weather_request:

        print('Getting weather for ' + weather_request.city + ' for the last ' + str(weather_request.period) + ' days')
        print('Posting: ' + url.format(weather_request.city, weather_request.period))
        r = requests.get(url.format(weather_request.city, weather_request.period)).json()

        print(r)

        print('Appending today\'s weather...')
        city_weather = {
            'city': weather_request.city,
            'icon': r['current']['condition']['icon'],
            'description': r['current']['condition']['text'],
            'temperature': r['current']['temp_c'],
            'humidity': r['current']['humidity'],
            'date': 'Today'
        }
        weather_data.append(city_weather)

        print('Appending weather forecast for next ' + str(len(r['forecast']['forecastday'])) + ' days')
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
                # 'description': r['weather'][0]['description'],
                # 'humidity': r['main']['humidity'],
                # 'icon': r['weather'][0]['icon'],
            }
            weather_data.append(city_weather)

        #   conn = sqlite3.connect('db.sqlite3')
        #   c = conn.cursor()
        #   c.execute('''insert into weatherapi_humdity values(?)''', (json.dumps(r['main']['humidity']),
        #                                                            conn.commit()))

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)
