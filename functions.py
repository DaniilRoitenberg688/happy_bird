import os
import sys

from objects import *


def new_tube(group, empty):
    up = TubeUp(speed=-2, group=group)
    between = randrange(100, 350)
    TubeDown(speed=-2, group=group, between=between, high_up=up.rect.size[-1])
    EmptyTube(speed=-2, group=empty, high=between, y=up.rect.size[-1])


def create_running_enemy(player_y):
    random = randrange(1, 101)
    if random % 3 == 0:
        HealthRunningEnemy(health_enemies, player_y)
        return
    RunningEnemy(enemies_group, player_y)


def load_image(name, colorkey=None):
    """Функция для загрузки изображения"""
    fullname = os.path.join('data/images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_hears(screen: pygame.display, col, image):
    if col == 1:
        screen.blit(image, (235, 0))

    if col == 2:
        screen.blit(image, (212, 0))
        screen.blit(image, (248, 0))

    if col == 3:
        screen.blit(image, (195, 0))
        screen.blit(image, (235, 0))
        screen.blit(image, (275, 0))
