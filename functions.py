import os
import sys

from objects import PiuingEnemy, TubeUp, TubeDown, EmptyTube
from constants import *

import pygame
from random import randrange
from groups import *


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
        if type(sprite) != PiuingEnemy:
            sprite.kill()


def change_walls_direction():
    for sprite in tube_group:
        sprite.speed_x *= -1

    for sprite in empty_tubes:
        sprite.speed_x *= -1


def draw_win_menu(screen, x, y, points):

    font_for_lose = pygame.font.Font('data/fonts/FlappyBirdRegular.ttf', 100)
    press_any_key = pygame.font.Font('data/fonts/FlappyBirdRegular.ttf', 50)
    font_for_points = pygame.font.Font('data/fonts/FlappyBirdRegular.ttf', 200)

    lose_text = font_for_lose.render('YOU LOSE', True, RED)
    press_any_key_text = press_any_key.render('PRESS ANY KEY', True, GREY)
    text = str(points)
    points_text = font_for_points.render(text, True, BLACK)
    size = points_text.get_size()

    pygame.draw.rect(screen, PLATINUM, (x, y, 400, 400))
    screen.blit(lose_text, (x + (200 - lose_text.get_size()[0] // 2), y + 30))
    screen.blit(points_text, (x + (200 - size[0] // 2), y + 120))
    screen.blit(press_any_key_text, (x + (200 - press_any_key_text.get_size()[0] // 2), y + 320))


def clear():
    for i in tube_group:
        i.kill()

    for i in player_group:
        i.kill()

    for i in enemies_group:
        i.kill()

    for i in piu_group:
        i.kill()

    for i in empty_tubes:
        i.kill()

    for i in enemy_piu_group:
        i.kill()

    for i in health_enemies:
        i.kill()

    for i in add_patrons_group:
        i.kill()

    for i in all_sprites:
        i.kill()





