import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


def load_data(city, selected_date = None):
    params = {
        'key': API_KEY, 
        'q': city, 
        'aqi': 'yes', 
        'days': 1, 
        'alerts': 'no',
        #'days': 1
    }

    if selected_date:
        params['dt'] = selected_date
    else:
        params['days'] = 1

    response = requests.get(API_URL, params=params)
    #response = requests.get(API_URL, params={'key': API_KEY, 'q': city, 'aqi': 'yes', 'days': 1, 'alerts': 'no'})
    data = response.json()

    forecast_day = data['forecast']['forecastday'][0]   
    city_name = data['location']['name']
    temp = data['current']['temp_c']
    condition = data['current']['condition']['text']
    icon = data['current']['condition']['icon']

    forecast_hours = data['forecast']['forecastday'][0]['hour']
    hours = [hour['time'][-5:] for hour in forecast_hours]
    co = [hour["air_quality"]['co'] for hour in forecast_hours]
    no2 = [hour["air_quality"]['no2'] for hour in forecast_hours]
    o3 = [hour["air_quality"]['o3'] for hour in forecast_hours]
    so2 = [hour["air_quality"]['so2'] for hour in forecast_hours]
    pm2_5 = [hour["air_quality"]['pm2_5'] for hour in forecast_hours]
    pm10 = [hour["air_quality"]['pm10'] for hour in forecast_hours]

    return {
        'city_name': city_name,
        'temp': temp,
        'condition': condition,
        'icon': icon,
        'co': co,
        'no2': no2,
        'o3': o3,
        'so2': so2,
        'pm2_5': pm2_5,
        'pm10': pm10,
        'hours': hours,
        'date': forecast_day['date']}


    
