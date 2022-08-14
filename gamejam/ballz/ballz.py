import sys
import collections
import pygame as pg
import random


Size = collections.namedtuple("Size", ['width', 'height'])
Speed = collections.namedtuple("Speed", ["horz", "vert"])
    

size = Size(120*8, 120*5)
speed = Speed(1, 1)
black = 0, 0, 0


pg.init()
screen = pg.display.set_mode(size)
ball = pg.image.load("intro_ball.gif")
randomstart = random.randint(1, size.width-10), random.randint(1, size.height-10)
ballrect = ball.get_rect(center=randomstart)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > size.width:
        speed = Speed(-speed.horz, speed.vert)
    if ballrect.top < 0 or ballrect.bottom > size.height:
        speed = Speed(speed.horz, -speed.vert)

    screen.fill(black)
    screen.blit(ball, ballrect)
    pg.display.flip()
