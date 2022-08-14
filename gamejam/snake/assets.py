from gamejam import pygame
from gamejam.games.snake import game as Game


_opposites = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}


def get_snake():
    gz = Game.grid_size()
    win = Game.window()
    pos = (Game.snap(0.5, win.w-gz, gz), Game.snap(0.5, win.h-gz, gz))
    s = pygame.Rect(*pos, gz, gz)
    body = [s, s.move(gz, 0), s.move(gz*2, 0)]

    snake = {
        "dead": False,
        "length": 3,
        "belly": 0,
        "body": body,
        "direction": "RIGHT"
    }
    return snake


def moves(key: str=None):
    gz = Game.grid_size()
    directions = {
        "UP": (0, -gz),
        "DOWN": (0, gz),
        "LEFT": (-gz, 0),
        "RIGHT": (gz, 0)
    }
    return directions.get(key)


def valid_direction(current, direction):
    same_direction = current == direction
    opposite_direction = direction == _opposites[current]
    return current if (same_direction or opposite_direction) else direction


def step(snake, move=None):
    snake['direction'] = valid_direction(snake['direction'], move) if move else snake['direction']
    coordinates = moves(snake['direction'])
    head = snake['body'][-1]
    snake['body'].append(head.move(*coordinates))
    if collision(snake):
        snake['dead'] = True
    
    return snake


def collidewall(body):
    return not Game.window().contains(body[-1])


def collideself(body):
    return body[-1].collidelistall(body[:-1])


def collision(snake):
    body = snake['body']
    return True if collidewall(body) or collideself(body) else False
    

def bite(snake, apple):
    return snake['body'][-1].colliderect(apple)


def get_apple():
    gz = Game.grid_size()
    xy = Game.random_position()
    return pygame.Rect(*xy, gz, gz)


def get_valid_apple(body):
    valid_position = False
    while not valid_position:
        apple = get_apple()
        if not apple.collidelistall(body):
            valid_position = True
    return apple
