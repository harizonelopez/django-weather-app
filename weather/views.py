from django.shortcuts import render
import requests
from .config import API_KEY
from django.contrib import messages


def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def get_weather_icon(icon_code):
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

def home(request):
    weather_data = None
    error = None
    if 'city' in request.GET:
        city = request.GET['city']
        weather_data = get_weather_data(city)
        
        if weather_data.get('cod') == '404':
            error = f"{city} city not found. Please try again."
            messages.warning(request, error)
            weather_data = None

        elif weather_data:
            weather_data['weather'][0]['icon_url'] = get_weather_icon(weather_data['weather'][0]['icon'])
    
    return render(request, 'home.html', {'weather_data': weather_data})
