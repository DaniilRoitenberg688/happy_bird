import pygame.sprite

from constants import *
from functions import *

from random import randrange


def very_big_change(group_for_rotation: pygame.sprite.Group):
    sprite: pygame.sprite.Sprite

    for sprite in group_for_rotation:
        sprite.rect.x, sprite.rect.y = sprite.rect.x


def main():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))

    running = True

    clock = pygame.time.Clock()

    wall_counter = 0

    while running:
        screen.fill(SKY_BLUE)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        wall_counter += 1

        if wall_counter == 100:
            new_tube(tube_group, empty_tubes)
            wall_counter = 0

        tube_group.update()

        tube_group.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()