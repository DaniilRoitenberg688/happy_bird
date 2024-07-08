from random import randrange

import pygame.sprite

from functions import new_tube, draw_hearts, kill_everything, change_walls_direction, draw_win_menu, clear

from constants import *
from objects import Player, load_image, PiuingEnemy, create_running_enemy

from groups import *


def game_play():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))

    screen.fill(BLACK)
    pygame.display.flip()
    running = True

    now_rotation = 0

    player = Player(player_group, now_rotation)

    clock = pygame.time.Clock()

    counter_for_walls = 0
    counter_for_enemies = 0

    points = 0

    font_for_points = pygame.font.Font('data/fonts/FlappyBirdRegular.ttf', 65)
    font_for_patrons = pygame.font.Font('data/fonts/FlappyBirdRegular.ttf', 65)

    piu_enemy = 0
    piu_enemy_counter = 0
    is_piu_enemy = False

    heart_image = load_image('heart.png', -1)
    background = load_image('background.png')

    wait_piu_enemy = randrange(500, 1000)
    wait_wall = randrange(150, 250)
    wait_running_enemy = randrange(150, 250)

    piu_enemy_life = 0

    could_we_spawn_running_enemy = True

    new_tube(tube_group, empty_tubes, now_rotation)

    count_spaces = 0
    count_up_press = 0

    how_much_to_click_up = randrange(20, 40)
    how_much_to_click_space = randrange(5, 10)

    count_to_change_gravity = randrange(10, 20)

    show_end_table = False

    while running:
        screen.fill(SKY_BLUE)
        screen.blit(background, (0, 0))
        event_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                clear()

            if show_end_table:
                if event.type == pygame.KEYDOWN:
                    running = False
                    clear()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and player.patrons:
                    player.shot(piu_group)
                    count_spaces += 1

                if event.key == pygame.K_ESCAPE:
                    player.is_cheat = not player.is_cheat

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    count_up_press += 1

                if event.key == pygame.K_0 and now_rotation != 0:
                    kill_everything()
                    change_walls_direction()
                    if is_piu_enemy:
                        piu_enemy.is_killed = True
                        piu_enemy_counter = wait_piu_enemy - 50
                    is_piu_enemy = False
                    could_we_spawn_running_enemy = True
                    counter_for_enemies = 0
                    now_rotation = 0

                if event.key == pygame.K_2 and now_rotation != 2:
                    kill_everything()
                    change_walls_direction()
                    if is_piu_enemy:
                        piu_enemy.is_killed = True
                        piu_enemy_counter = wait_piu_enemy - 50
                    is_piu_enemy = False
                    could_we_spawn_running_enemy = True
                    counter_for_enemies = 0
                    now_rotation = 2

        counter_for_walls += 1
        counter_for_enemies += 1
        piu_enemy_counter += 1

        if count_up_press >= how_much_to_click_up and count_spaces >= how_much_to_click_space:
            count_up_press = 0
            count_spaces = 0

            how_much_to_click_up = randrange(20, 40)
            how_much_to_click_space = randrange(10, 20)

            kill_everything()
            change_walls_direction()
            if is_piu_enemy:
                piu_enemy.is_killed = True
            is_piu_enemy = False
            piu_enemy_counter = wait_piu_enemy - 50
            could_we_spawn_running_enemy = True
            counter_for_enemies = 0

            if now_rotation == 0:
                now_rotation = 2
            else:
                now_rotation = 0

        if player.hp <= 0:
            player.is_alive = False
            show_end_table = True

        if is_piu_enemy and piu_enemy_life <= 100:
            piu_enemy_life += 1

        if piu_enemy_life >= 100 and not could_we_spawn_running_enemy:
            could_we_spawn_running_enemy = True
            counter_for_enemies = 0
            piu_enemy_life = 0

        if piu_enemy_counter == wait_piu_enemy:
            piu_enemy = PiuingEnemy(enemies_group, player.rect.y, now_rotation)
            is_piu_enemy = True
            could_we_spawn_running_enemy = False

        if is_piu_enemy and piu_enemy.hp == 0:
            is_piu_enemy = False
            could_we_spawn_running_enemy = True
            piu_enemy_counter = 0
            counter_for_enemies = 50
            piu_enemy_life = 0
            wait_piu_enemy = randrange(500, 1000)

        if counter_for_walls == wait_wall:
            new_tube(tube_group, empty_tubes, now_rotation)
            counter_for_walls = 0
            wait_wall = randrange(100, 200)

        if could_we_spawn_running_enemy and counter_for_enemies == wait_running_enemy:
            create_running_enemy(player.rect.y, now_rotation)
            counter_for_enemies = 0
            wait_running_enemy = randrange(150, 250)

        is_collide_tube = pygame.sprite.spritecollideany(player, tube_group)
        is_collide_enemy = pygame.sprite.spritecollideany(player, enemies_group)
        is_collide_piu = pygame.sprite.spritecollideany(player, enemy_piu_group)
        is_collide_health_enemy = pygame.sprite.spritecollideany(player, health_enemies)
        is_collide_add_patrons = pygame.sprite.spritecollideany(player, add_patrons_group)

        if not player.is_cheat:
            if is_collide_tube:
                player.hp = 0

            if is_collide_enemy:
                is_collide_enemy.kill()
                player.hp -= 1

            if is_collide_piu:
                is_collide_piu.kill()
                player.hp -= 1

            if is_collide_health_enemy:
                if player.hp < 5:
                    player.hp += 1
                is_collide_health_enemy.kill()

            if is_collide_add_patrons:
                is_collide_add_patrons.kill()
                player.patrons += 1

            if player.rect.y <= 0 or player.rect.y >= 500:
                player.hp = 0

        empty_tube = pygame.sprite.spritecollideany(player, empty_tubes)
        if empty_tube:
            points += 1
            empty_tube.kill()
            if points and points % 3 == 0:
                player.patrons += 1

        if not player.is_alive:
            show_end_table = True

        points_text = font_for_points.render(str(points), True, WHITE)
        patrons_text = font_for_patrons.render(str(player.patrons), True, WHITE)

        if not show_end_table:
            tube_group.update()
            player_group.update(event_keys, now_rotation)
            enemies_group.update(now_rotation)
            health_enemies.update(piu_group)
            piu_group.update()
            enemy_piu_group.update(now_rotation)
            add_patrons_group.update()
            empty_tubes.update()

        tube_group.draw(screen)
        player_group.draw(screen)
        enemies_group.draw(screen)
        health_enemies.draw(screen)
        piu_group.draw(screen)
        enemy_piu_group.draw(screen)
        add_patrons_group.draw(screen)
        empty_tubes.draw(screen)

        draw_hearts(screen, player.hp, heart_image)

        screen.blit(points_text, (0, 0))
        screen.blit(patrons_text, (450, 0))

        if show_end_table:
            draw_win_menu(screen, 50, 50, points)

        pygame.display.flip()

        clock.tick(FPS)



if __name__ == '__main__':
    game_play()
