import argparse
import logging
from kivy.app import App
from kivy.uix.widget import Widget

class PongGame(Widget):
    pass


class PongApp(App):
    def build(self):
        return PongGame()


def main():

    logger = logging.Logger("app")
    try:
        PongApp().run()
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()
