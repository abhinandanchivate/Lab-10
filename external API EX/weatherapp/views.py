
import requests # to raise the rest call
from django.conf import settings
from django.shortcuts import render

def weather_view(request):
    if request.method=='POST':
        city= request.POST.get('city')
        api_key = settings.API_KEY
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            weather_data={
                'city':data['name'],
                'temperature':data['main']['temp'],
                'description':data['weather'][0]['description'],
                'icon':data['weather'][0]['icon']
            }
        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP error occurred: {e}"
        except Exception as e:
            error_message = f"An error occurred: {e}"
    return render(request, 'weather/weather_result.html', {
        'weather': weather_data ,
        'error': error_message
    })
            


