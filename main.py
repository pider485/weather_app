from kivymd.uix.pickers.datepicker.datepicker import date
from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from config import API_KEY, API_URL, FORECAST_URL
import requests

class WeatherCard(MDCard):
    def __init__(self, data_time, description, icon, temp, rain, wind, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.date_text.text = data_time
        self.ids.desc_text.text = description
        self.ids.temp_text.text = f"{temp}°C"
        self.ids.rain_text.text = f"Ймовірність опадів: {rain*100}%"
        self.ids.wind_text.text = f"Швидкість вітру:{wind}м/с"
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_weather_data(self,url,city):
        api_params={
            "q": city,
            "appid": API_KEY
        }
        data = requests.get(url,api_params)
        
        if data.status_code == 200:    
            respon = data.json()
            return respon
        else:
            return None

    def add_weather_card(self,  respon):
        description = respon["weather"][0]["description"]
        icon = respon["weather"][0]["icon"]
        temp = respon["main"]["temp"]
        if 'rain' in respon:
            if "1h" in respon['rain']:
                rain = respon['rain']["1h"]
            else:
                rain = respon['rain']["3h"]
        else:
            rain= 0
        wind = respon["wind"]["speed"]
        if 'dt_txt' in respon:
            data_time = respon['dt_txt'][5:-3]
        else:
            data_time = "Зараз"
        new_card = WeatherCard (data_time,description,icon,temp,rain,wind)
        self.ids.Weather_carusel.add_widget(new_card)

    def weather_search(self):
        self.ids.Weather_carusel.clear_widgets()
        city = self.ids.city_field.text.strip().lower()
        curret_weather = self.get_weather_data(API_URL,city)
        forcast = self.get_weather_data(FORECAST_URL,city)
        
        if curret_weather:
            self.add_weather_card(curret_weather)
        
        if forcast:
            for period in forcast['list']:
                self.add_weather_card(period)

class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_file('style.kv')
        self.screen = MainScreen("main_screen")
        return self.screen

WeatherApp().run()