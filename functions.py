import os
import sys

from objects import *
from constants import *

import pygame


def new_tube(group, empty):
    up = TubeUp(speed=-2, group=group)
    between = randrange(100, 350)
    TubeDown(speed=-2, group=group, between=between, high_up=up.rect.size[-1])
    EmptyTube(speed=-2, group=empty, high=between, y=up.rect.size[-1])


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

