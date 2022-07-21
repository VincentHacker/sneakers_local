from datetime import datetime
import json
import requests

from config import token_weather

def get_weather(city, token_weather):

    smile_code = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token_weather}&units=metric'
        )
        data = req.json()

        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(data['sys']['sunset'])
        weather_decrip = data['weather'][0]['main']
        if weather_decrip in smile_code:
            wd = smile_code[weather_decrip]
        length_day = sunset - sunrise
        length_night = str(sunrise - sunset).split()[-1]

        data = (f'В городе: {city}\nТемпература: {cur_weather}C {wd}\nВлажность: {humidity}\nСкорость ветра: {wind}м/с\nРассвет в: {sunrise}\nЗакат в: {sunset}\nПродолжительность дня: {length_day}\nПродолжительность ночи: {length_night}')

        with open('/home/atai/Desktop/Bootcamp/week11/sneakers/TgBot/weather.json', 'w') as file:
            json.dump(data, file, indent=4)
        
        

    except Exception as ex:
        print(ex)
        print('Check cities name!')


def main():
    get_weather('bishkek', token_weather)


if __name__ == '__main__':
    main()
