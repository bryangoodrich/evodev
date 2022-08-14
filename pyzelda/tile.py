import pygame
from importlib import resources


def create(pos):
    with resources.path("pyzelda.graphics", "rock.png") as path:
        img = pygame.image.load(path).convert_alpha()
    
    sprite = {
        "image": img,
        "rect": img.get_rect(topleft = pos)
    }
    return sprite
