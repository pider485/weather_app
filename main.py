from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from config import API_KEY, API_URL
import requests

class WeatherCard(MDCard):
    def __init__(self, description, icon, temp, rain, wind, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.desc_text.text = description
        self.ids.temp_text.text = f"{temp}°C"
        self.ids.rain_text.text = f"Ймовірність опадів: {rain*100}%"
        self.ids.wind_text.text = f"Швидкість вітру:{wind}м/с"
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def weather_search(self):
        self.ids.Weather_carusel.clear_widgets()
        city = self.ids.city_field.text.strip().lower()
        api_params={
            "q": city,
            "appid": API_KEY
        }
        data = requests.get(API_URL,api_params)
        respon = data.json()
        print(respon)
        description = respon["weather"][0]["description"]
        icon = respon["weather"][0]["icon"]
        temp = respon["main"]["temp"]
        if 'rain' in respon:
            rain = respon["rain"]["1h"]
        else:
            rain= 0
        wind = respon["wind"]["speed"]

        new_card = WeatherCard (description,icon,temp,rain,wind)
        self.ids.Weather_carusel.add_widget(new_card)

class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_file('style.kv')
        self.screen = MainScreen("main_screen")
        return self.screen

WeatherApp().run()