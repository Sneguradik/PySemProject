from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(CustomScreenManager, self).__init__(**kwargs)


class AnalysisApp(App):
    def build(self):
        sm = CustomScreenManager()
        return sm
