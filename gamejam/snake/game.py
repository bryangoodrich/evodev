import random
from dataclasses import dataclass

from gamejam import Conf, pygame


keys = {
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN",
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT"
}


@dataclass(frozen=True)
class Color:
    RED = pygame.Color(200, 40, 0, 1)
    BLACK = pygame.Color(0, 0, 0, 1)
    WHITE = pygame.Color(255, 255, 255, 1)
    GREEN = pygame.Color(43, 255, 0, 1)


def grid_size():
    return Conf['cellsize']


def screen():
    return pygame.display.get_surface()


def window():
    return screen().get_rect()


def menu_scene(color=Color.WHITE):
    win = window()
    scr = screen()
    msg = "Press Q to QUIT, C to CONTINUE."
    font = pygame.font.SysFont(None, 50)
    center = (win.w / 2, win.h / 2)
    scr.fill(color)
    text = font.render(msg, True, Color.BLACK)
    rect = text.get_rect(center=center)
    scr.blit(text, rect)
    pygame.display.update()


def game_scene(color=Color.BLACK):
    scr = screen()
    scr.fill(color)
    pygame.display.update()


def dead_scene(ms, font_color=Color.RED, bg_color=Color.WHITE):
    win = window()
    scr = screen()
    msg = "YOU DIED!"
    scr.fill(bg_color)
    font = pygame.font.SysFont(None, 50)
    banner = pygame.Rect(0, win.centery-100, win.w, 200)
    pygame.draw.rect(scr, Color.BLACK, banner)
    text = font.render(msg, True, font_color)
    rect = text.get_rect(center=win.center)
    scr.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(ms)


def print_score(score, color=Color.GREEN):
    scr = screen()
    msg = f"Score: {score}"
    font = pygame.font.SysFont(None, 50)
    text = font.render(msg, True, color)
    rect = text.get_rect(topleft=(0,0))
    scr.blit(text, rect)
    pygame.display.update()


def print_generation(generation):
    scr = screen()
    msg = f"generation {generation}"
    smallfont = pygame.font.SysFont(None, 20)
    text = smallfont.render(msg, True, Color.RED)
    rect = text.get_rect(topleft=(0, 50))
    scr.blit(text, rect)
    pygame.display.update()


def print_ttl(x):
    scr = screen()
    msg = f"TTL: {x}"
    smallfont = pygame.font.SysFont(None, 20)
    text = smallfont.render(msg, True, Color.RED)
    rect = text.get_rect(topleft=(0, 580))
    scr.blit(text, rect)
    pygame.display.update()


def snap(p, upr, size):
    return round(p*upr / size)*size


def random_position(width=None, height=None):
    gz = grid_size()
    win = window()
    width = width if width else win.w
    height = height if height else win.h
    x = snap(random.random(), width-gz, gz)
    y = snap(random.random(), height-gz, gz)
    return x, y


def draw(rect, color):
    pygame.draw.rect(screen(), color, rect)
    pygame.display.update()


def menu_controller(state):
    for event in pygame.event.get():
        exit = (
            event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_q)
        )
        if exit:
            state['gameover'] = True
            state['paused'] = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            state['paused'] = False


def game_controller(state):
    for event in pygame.event.get():
        exit = event.type == pygame.QUIT
        paused = event.type == pygame.KEYDOWN and event.key == pygame.K_p
        if exit:
            state['gameover'] = True
            raise SystemExit

        if paused:
            state['paused'] = True

        if event.type == pygame.KEYDOWN:
            return keys.get(event.key)

    return None
