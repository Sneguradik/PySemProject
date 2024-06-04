import configparser
import os
from typing import Dict, Any
import tkinter as tk
from tkinter import font as tkFont


def read_config() -> Dict[str, Any]:
    config = configparser.ConfigParser()

    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf.ini'))

    return {
        "font": {
            "type": config['Font']['type'],
            "size": int(config['Font']['size']),
        },
        "color": {
            "background": config['Colors']['background'],
            "primary3": config['Colors']['primary3'],
            "primary2": config['Colors']['primary2'],
            "primary1": config['Colors']['primary1'],
        }
    }


conf = read_config()


def get_font() -> tkFont.Font:
    return tkFont.Font(family=conf['font']['type'], size=conf['font']['size'] , weight="bold")
