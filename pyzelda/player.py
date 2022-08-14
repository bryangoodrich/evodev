import pygame
from importlib import resources


def create(pos):
    with resources.path("pyzelda.graphics", "player.png") as path:
        img = pygame.image.load(path).convert_alpha()
    
    player = {
        "image": img,
        "rect": img.get_rect(topleft = pos),
        "direction": pygame.math.Vector2(),
        "speed": 5
    }
    return player

    
def move(actor, obstacles):
    if actor['direction'].magnitude() != 0:
        actor['direction'] = actor['direction'].normalize()
    
    actor['rect'].x += actor['direction'].x * actor['speed']
    actor = collide(actor, obstacles, True)
    actor['rect'].y += actor['direction'].y * actor['speed']
    actor = collide(actor, obstacles, False)
    return actor


def input(actor):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        actor['direction'].y = -1
    elif keys[pygame.K_DOWN]:
        actor['direction'].y = 1
    else:
        actor['direction'].y = 0
    
    if keys[pygame.K_LEFT]:
        actor['direction'].x = -1
    elif keys[pygame.K_RIGHT]:
        actor['direction'].x = 1
    else:
        actor['direction'].x = 0
    
    return actor


def update(actor, obstacles):
    actor = input(actor)
    actor = move(actor, obstacles)
    return actor


def collide_horizontal(actor, sprites):
    for sprite in sprites:
        if sprite['rect'].colliderect(actor['rect']):
            if actor['direction'].x > 0:
                actor['rect'].right = sprite['rect'].left
            if actor['direction'].x < 0:
                actor['rect'].left = sprite['rect'].right
    return actor


def collide_vertical(actor, sprites):
    for sprite in sprites:
        if sprite['rect'].colliderect(actor['rect']):
            if actor['direction'].y > 0:
                actor['rect'].bottom = sprite['rect'].top
            if actor['direction'].y < 0:
                actor['rect'].top = sprite['rect'].bottom
    return actor


def collide(actor, sprites, sideways=True):
    return collide_horizontal(actor, sprites) if sideways else collide_vertical(actor, sprites)
