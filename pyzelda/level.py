import pygame
from pyzelda import settings as Settings
from pyzelda import tile as Tile
from pyzelda import player as Player
from pyzelda import debug as Debug


def create_map(sprites):
    for i, row in enumerate(Settings.WORLD_MAP):
        for j, col in enumerate(row):
            x = j * Settings.TILESIZE
            y = i * Settings.TILESIZE
            if col == 'x':
                sprites['tiles'].append(Tile.create((x, y)))
            if col == 'p':
                sprites['player'] = Player.create((x, y))
    return sprites


def create():
    sprites = {
        "tiles": [],
        "player": None
    }
    sprites = create_map(sprites)
    return sprites


def draw(sprite):
    screen = pygame.display.get_surface()
    screen.blit(sprite['image'], sprite['rect'])


def draws(sprites):
    for sprite in sprites:
        draw(sprite)


def update(sprites):
    player = sprites['player']
    obstacles = sprites['tiles']
    draws(obstacles)
    draw(player)
    player = Player.input(player)
    player = Player.move(player, obstacles)
    sprites['player'] = player
    return sprites


