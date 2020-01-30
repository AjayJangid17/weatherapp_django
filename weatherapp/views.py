from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    urls = 'http://openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=b6907d289e10d714a6e88b30761fae22'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(urls.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist'
            else:
                err_msg = 'City already exist in the database'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(urls.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

        # print(weather_data)

    context = {
            'weather_data': weather_data,
            'form': form,
            'message' : message,
            'message_class': message_class
    }
    return render(request,'weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect(index)
