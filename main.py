from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from config import API_KEY, API_URL
import requests

class WeatherCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def weather_search(self):
        city = self.ids.city_field.text.strip().lower()
        api_params={
            "q": city,
            "appid": API_KEY
        }
        data = requests.get(API_URL,api_params)
        respon = data.json()
        print(respon)
        description = respon["weather"][0]["description"]
        self.ids.Weather_card.ids.label.text = description

class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_file('style.kv')
        self.screen = MainScreen("main_screen")
        return self.screen

WeatherApp().run()