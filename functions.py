import os
import sys

from objects import *
from constants import *

import pygame
from random import randrange
from groups import enemies_group, enemy_piu_group, tube_group, empty_tubes


def new_tube(group, empty, rotation):
    up = TubeUp(speed=-2, group=group, rotation=rotation)
    between = randrange(100, 250)
    TubeDown(speed=-2, group=group, between=between, high_up=up.random_pos, rotation=rotation)
    EmptyTube(speed=-2, group=empty, high=between, y=up.random_pos, rotation=rotation)


def draw_hearts(screen: pygame.display, col, image):
    if col == 1:
        screen.blit(image, (235, 0))

    if col == 2:
        screen.blit(image, (212, 0))
        screen.blit(image, (248, 0))

    if col == 3:
        screen.blit(image, (199, 0))
        screen.blit(image, (235, 0))
        screen.blit(image, (271, 0))

    if col == 4:
        screen.blit(image, (176, 0))
        screen.blit(image, (212, 0))
        screen.blit(image, (248, 0))
        screen.blit(image, (284, 0))

    if col == 5:
        screen.blit(image, (163, 0))
        screen.blit(image, (199, 0))
        screen.blit(image, (235, 0))
        screen.blit(image, (271, 0))
        screen.blit(image, (307, 0))


def kill_everything():
    for sprite in enemies_group:
        sprite.kill()

    for sprite in enemy_piu_group:
        sprite.kill()


def change_walls_direction():
    for sprite in tube_group:
        sprite.speed_x *= -1

    for sprite in empty_tubes:
        sprite.speed_x *= -1



