import pygame.sprite

from functions import *


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
    piu_enemy_counter = 0
    is_piu_enemy = False

    heart_image = load_image('heart.png', -1)

    background = load_image('space.png')

    while running:
        screen.blit(background, (0, 0))

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
        piu_enemy_counter += 1

        if player.hp <= 0:
            running = False

        if piu_enemy_counter == 500:
            piu_enemy = PiuingEnemy(enemies_group, player.rect.y)
            is_piu_enemy = True

        if is_piu_enemy and piu_enemy.hp == 0:
            is_piu_enemy = False
            piu_enemy_counter = 0
            counter_for_enemies = 50

        if counter_for_walls == 100:
            new_tube(tube_group, empty_tubes)
            counter_for_walls = 0

        if counter_for_enemies == 150 and not is_piu_enemy:
            create_running_enemy(player.rect.y)
            counter_for_enemies = 0

        is_collide_tube = pygame.sprite.spritecollideany(player, tube_group)
        is_collide_enemy = pygame.sprite.spritecollideany(player, enemies_group)
        is_collide_piu = pygame.sprite.spritecollideany(player, enemy_piu_group)
        is_collide_health_enemy = pygame.sprite.spritecollideany(player, health_enemies)

        if not player.is_cheat:
            if is_collide_tube:
                player.hp = 0

            if is_collide_enemy:
                player.hp -= 1
                is_collide_enemy.kill()

            if is_collide_piu:
                player.hp -= 1
                is_collide_piu.kill()

            if is_collide_health_enemy:
                if player.hp < 3:
                    player.hp += 1
                is_collide_health_enemy.kill()

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
        health_enemies.update(piu_group)
        piu_group.update()
        enemy_piu_group.update()
        empty_tubes.update()

        tube_group.draw(screen)
        player_group.draw(screen)
        enemies_group.draw(screen)
        health_enemies.draw(screen)
        piu_group.draw(screen)
        enemy_piu_group.draw(screen)
        empty_tubes.draw(screen)

        draw_hears(screen, player.hp, heart_image)

        screen.blit(points_text, (0, 0))
        screen.blit(patrons_text, (450, 0))

        pygame.display.update()

        clock.tick(FPS)


if __name__ == '__main__':
    main()
