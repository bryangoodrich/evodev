import pygame
import sys
from pyzelda import settings as Settings
from pyzelda import level as Level


def main():
    pygame.init()
    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    pygame.display.set_caption("Python Zelda")
    clock = pygame.time.Clock()

    gameover = False
    game = Level.create()
    while not gameover:
        for event in pygame.event.get():
            exit = (
                event.type == pygame.QUIT
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_q)
            )
            if exit:
                gameover = True
                pygame.quit()
                sys.exit()

        screen.fill('black')
        game = Level.update(game)
        pygame.display.update()
        clock.tick(Settings.FPS)

if __name__ == "__main__":
    main()
