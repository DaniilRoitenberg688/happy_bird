from random import randrange
import os
import sys

from constants import *
from groups import *
from objects import TubeUp, TubeDown, Player, FirstEnemy, EmptyTube, SecondEnemy


def new_tube(group, empty):
    up = TubeUp(speed=-2, group=group)
    between = randrange(100, 350)
    TubeDown(speed=-2, group=group, between=between, high_up=up.rect.size[-1])
    EmptyTube(speed=-2, group=empty, high=between, y=up.rect.size[-1])


def load_image(name, colorkey=None):
    """Функция для загрузки изображения"""
    fullname = os.path.join(name)
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




def main():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))

    running = True

    player = Player(player_group)

    clock = pygame.time.Clock()
    new_tube(tube_group, empty_tubes)

    counter_for_walls = 0
    counter_for_enemies = 0

    points = 0

    font_for_points = pygame.font.Font(None, 65)
    font_for_patrons = pygame.font.Font(None, 65)

    piu_enemy = 0
    piu_counter = 0
    is_piu_enemy = False

    heart_image = load_image('heart.png', -1)

    while running:
        screen.fill(SKY_BLUE)

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.patrons:
                    player.shot(piu_group)

                if event.key == pygame.K_ESCAPE:
                    player.is_cheat = not player.is_cheat

        counter_for_walls += 1
        counter_for_enemies += 1
        piu_counter += 1

        if player.hp <= 0:
            running = False

        if piu_counter == 500:
            piu_enemy = SecondEnemy(enemies_group, player.rect.y)
            is_piu_enemy = True

        if is_piu_enemy and piu_enemy.hp == 0:
            is_piu_enemy = False
            piu_counter = 0
            counter_for_enemies = 50

        print(is_piu_enemy)

        if counter_for_walls == 100:
            new_tube(tube_group, empty_tubes)
            counter_for_walls = 0

        if counter_for_enemies == 150 and not is_piu_enemy:
            FirstEnemy(group=enemies_group, y=player.rect.y)
            counter_for_enemies = 0

        # if not player.is_cheat and (pygame.sprite.spritecollideany(player, tube_group) or pygame.sprite.spritecollideany(player, enemies_group)\
        #         or pygame.sprite.spritecollideany(player, enemy_piu)):
        #     player.hp -= 1

        empty_tube = pygame.sprite.spritecollideany(player, empty_tubes)
        if empty_tube:
            points += 1
            empty_tube.kill()
            if points and points % 3 == 0:
                player.patrons += 1

        points_text = font_for_points.render(str(points), True, BLACK)
        patrons_text = font_for_patrons.render(str(player.patrons), True, BLACK)

        tube_group.update()
        player_group.update(keys)
        enemies_group.update(piu_group)
        piu_group.update()
        enemy_piu.update()
        empty_tubes.update()

        tube_group.draw(screen)
        player_group.draw(screen)
        enemies_group.draw(screen)
        piu_group.draw(screen)
        enemy_piu.draw(screen)
        empty_tubes.draw(screen)

        draw_hears(screen, player.hp, heart_image)

        screen.blit(points_text, (0, 0))
        screen.blit(patrons_text, (450, 0))

        pygame.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
