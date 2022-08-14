"""
The snake goes hissssssss
"""

version = "0.1"
__version__ = version


import pygame
import yaml


def load_settings(settings="settings.conf"):
    try:
        with open(settings, 'r') as fh:
            conf = yaml.safe_load(fh)
        
        return conf
    except FileNotFoundError:
        print("Default settings file 'settings.conf' not found.")
        return None


Conf = load_settings()
