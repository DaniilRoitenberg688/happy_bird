import pygame.draw

from functions import *
from groups import *

from random import randrange

from constants import *


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


def create_running_enemy(player_y, rotation):
    random = randrange(1, 101)
    if random % 3 == 0:
        HealthRunningEnemy(health_enemies, player_y, rotation)
        return
    RunningEnemy(enemies_group, player_y, rotation)


class TubeUp(pygame.sprite.Sprite):
    def __init__(self, speed, group, rotation):
        super().__init__(all_sprites, group)

        if rotation == 0 or rotation == 2:
            self.image = load_image('tube.png')
        self.rotation = rotation

        self.rect = self.image.get_rect()

        self.random_pos = randrange(50, 350)

        if self.rotation == 0:
            self.rect.x = 500
            self.rect.y = self.random_pos - 375
            self.speed_x = speed
            self.speed_y = 0

        if self.rotation == 2:
            self.rect.x = -50
            self.rect.y = self.random_pos - 375
            self.speed_x = -speed
            self.speed_y = 0

    def update(self, *args, **kwargs):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x < -50 or self.rect.x > 550:
            self.kill()


class TubeDown(pygame.sprite.Sprite):
    def __init__(self, speed, group, between, high_up, rotation):
        super().__init__(all_sprites, group)

        high = SIZE - between - high_up

        if high < 0:
            self.kill()
            return

        self.rotation = rotation

        if rotation == 0 or rotation == 2:
            self.image = load_image('tube.png')

        self.rect = self.image.get_rect()

        if self.rotation == 0:
            self.rect.x = 500
            self.rect.y = between + high_up
            self.speed_x = speed
            self.speed_y = 0

        if self.rotation == 2:
            self.rect.x = -50
            self.rect.y = between + high_up
            self.speed_x = -speed
            self.speed_y = 0

    def update(self, *args, **kwargs):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x < -50 or self.rect.x > 550:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, group, rotation):
        super().__init__(group)

        # self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # self.image = self.image.convert_alpha()
        # pygame.draw.circle(self.image, GOLD, (10, 10), 10)

        self.sprites = [load_image('bird/0.png'),
                        load_image('bird/1.png'),
                        load_image('bird/2.png')]

        self.flipped_sprites = []

        for image in self.sprites:
            self.flipped_sprites.append(pygame.transform.flip(image, False, True))

        self.image = self.sprites[0]

        self.rect = self.image.get_rect()

        self.rotation = rotation

        self.rect.x = 231
        self.rect.y = 250

        self.is_jump = 0

        self.patrons = 12

        self.counter = 0

        self.gravity = -5

        self.is_cheat = False

        self.hp = 3

        self.up_or_down = 1

        self.is_alive = True

        self.current_image = 0

        self.killed = False

    def update(self, *args, **kwargs):
        keys = args[0]
        rotation = args[1]

        if self.is_alive:
            if self.rotation != rotation:
                for i in range(len(self.sprites)):
                    self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)
                    self.flipped_sprites[i] = pygame.transform.flip(self.sprites[i], True, False)

            self.rotation = rotation

            if self.current_image % 10 == 0:
                self.image = self.sprites[self.current_image // 7]

            if self.current_image > 20:
                self.current_image = 0

            self.current_image += 1

            if not self.is_cheat:

                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    self.is_jump = 5
                    self.gravity = 3 * self.up_or_down

                if self.is_jump:
                    self.rect.y -= self.is_jump * 2 * self.up_or_down
                    self.is_jump -= 1

                if not self.is_jump:
                    self.gravity = 5 * self.up_or_down

                self.rect.y += self.gravity

            else:
                if keys[pygame.K_UP]:
                    self.rect.y -= 4
                if keys[pygame.K_DOWN]:
                    self.rect.y += 4
        else:
            self.gravity = 6
            self.rect.y += self.gravity

    def shot(self, group):
        Piu(group=group, x=self.rect.x + 5, y=self.rect.y, rotation=self.rotation)
        self.patrons -= 1


class RunningEnemy(pygame.sprite.Sprite):
    def __init__(self, group, y, rotation):
        super().__init__(all_sprites, group)

        self.sprites = [load_image('fb/fb0.png'), load_image('fb/fb1.png'), load_image('fb/fb2.png'),
                        load_image('fb/fb3.png'), load_image('fb/fb4.png')]

        if rotation == 0:
            for i in range(len(self.sprites)):
                self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)

        self.image = self.sprites[0]

        self.rect = self.image.get_rect()

        self.right_image = self.image

        self.degree = 0

        self.current_image = 0

        self.rotation = rotation

        if rotation == 0:
            self.rect.x = 500
            self.rect.y = y
            self.speed = -5

        if rotation == 2:
            self.rect.x = 1
            self.rect.y = y
            self.speed = 5

        self.hp = 1

    def update(self, *args, **kwargs):
        self.rect.x += self.speed
        rotation = args[0]
        if self.rotation != rotation:
            self.rotation = rotation
            for i in range(len(self.sprites)):
                self.sprites[i] = pygame.transform.flip(self.sprites[i], True, False)

        if self.current_image % 5 == 0:
            self.image = self.sprites[self.current_image // 5]

        if self.rect.x < 0 or self.rect.x > 500:
            self.kill()

        self.current_image += 1
        if self.current_image > 20:
            self.current_image = 0


class Piu(pygame.sprite.Sprite):
    def __init__(self, group, x, y, rotation):
        super().__init__(all_sprites, group)

        # self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        # self.image = self.image.convert_alpha()
        # pygame.draw.circle(self.image, GOLD, (6, 6), 6)

        self.image = load_image('red.png')

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        if rotation == 0:
            self.speed = 7

        if rotation == 2:
            self.speed = -7

            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, *args, **kwargs):
        self.rect.x += self.speed
        if self.rect.x > 500 or self.speed < -50:
            self.kill()

        enemies_piu = pygame.sprite.spritecollideany(self, enemy_piu_group)
        if enemies_piu:
            self.speed *= -1
            enemies_piu.speed *= -1
            new_piu = EnemyPiu(piu_group, enemies_piu.rect.x, enemies_piu.rect.y, speed=enemies_piu.speed)
            enemies_piu.kill()


class EmptyTube(pygame.sprite.Sprite):
    def __init__(self, group, y, high, speed, rotation):
        super().__init__(all_sprites, group)

        if rotation == 0 or rotation == 2:
            self.image = pygame.Surface((50, high), pygame.SRCALPHA)

        self.rotation = rotation
        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()

        if self.rotation == 0:
            self.rect.x = 500
            self.rect.y = y
            self.speed_x = speed
            self.speed_y = 0

        if self.rotation == 2:
            self.rect.x = -50
            self.rect.y = y
            self.speed_x = -speed
            self.speed_y = 0

    def update(self, *args, **kwargs):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x < -50 or self.rect.x > 550:
            self.kill()


class PiuingEnemy(pygame.sprite.Sprite):
    def __init__(self, group, y, rotation):
        super().__init__(all_sprites, group)

        # self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # self.image = self.image.convert_alpha()
        # pygame.draw.circle(self.image, MUSLIM_GREEN, (20, 20), 20)

        self.flying_sprites = [load_image('enemy/flying/0.png'),
                               load_image('enemy/flying/1.png'),
                               load_image('enemy/flying/2.png'),
                               load_image('enemy/flying/3.png')]

        self.death_sprites = [load_image('enemy/death/0.png'),
                              load_image('enemy/death/1.png'),
                              load_image('enemy/death/2.png'),
                              load_image('enemy/death/3.png'),
                              load_image('enemy/death/4.png'),
                              load_image('enemy/death/5.png')]

        self.attack_sprites = [load_image('enemy/attack/0.png'),
                               load_image('enemy/attack/1.png'),
                               load_image('enemy/attack/2.png'),
                               load_image('enemy/attack/3.png'),
                               load_image('enemy/attack/4.png'),
                               load_image('enemy/attack/5.png'),
                               load_image('enemy/attack/6.png'),
                               load_image('enemy/attack/7.png')]

        self.is_killed = False

        self.kill_timer = 0

        self.image = self.flying_sprites[0]

        self.current_image = 0

        self.rect = self.image.get_rect()

        if rotation == 0:
            self.rect.x = 500
            self.rect.y = y

        if rotation == 2:
            self.rect.x = 0
            self.rect.y = y
            for i in range(len(self.flying_sprites)):
                self.flying_sprites[i] = pygame.transform.flip(self.flying_sprites[i], True, False)

            for i in range(len(self.death_sprites)):
                self.death_sprites[i] = pygame.transform.flip(self.death_sprites[i], True, False)

            for i in range(len(self.attack_sprites)):
                self.attack_sprites[i] = pygame.transform.flip(self.attack_sprites[i], True, False)

        self.rotation = rotation

        self.new_y = None

        self.speed = 2

        self.wait_counter = 0

        self.piu_or_not = False

        self.hp = 2

    def update(self, *args, **kwargs):

        rotation = args[0]

        if not self.is_killed:
            if self.rotation == 0:
                if self.rect.x > 400:
                    self.rect.x -= 3

            if self.rotation == 2:
                if self.rect.x < 30:
                    self.rect.x += 3

            self.rotation = rotation

            if self.hp == 0:
                self.is_killed = True

            piu_group_collision = pygame.sprite.spritecollideany(self, piu_group)
            if piu_group_collision:
                self.hp -= 1
                piu_group_collision.kill()

            if self.new_y is None:
                self.new_y = randrange(50, 450)

            elif self.new_y is not None:
                if abs(self.new_y - self.rect.y) <= 5:

                    if self.wait_counter % 7 == 0:
                        self.image = self.attack_sprites[self.wait_counter // 7]

                    if self.wait_counter == 50:
                        self.new_y = None
                        self.wait_counter = 0
                        self.piu_or_not = False

                    elif self.wait_counter == 25 and not self.piu_or_not:
                        if self.rotation == 0:
                            self.shot(self.rect.x, self.rect.y + 35)

                        if self.rotation == 2:
                            self.shot(self.rect.x + 35, self.rect.y + 35)

                        self.piu_or_not = True

                    else:
                        self.wait_counter += 1
                else:
                    if self.new_y > self.rect.y:
                        self.rect.y += self.speed
                    else:
                        self.rect.y -= self.speed

                    self.current_image += 1

                    if self.current_image % 7:
                        self.image = self.flying_sprites[self.current_image // 7]

                    if self.current_image > 7 * 3:
                        self.current_image = 0
        else:
            if self.kill_timer > 35:
                self.kill()

            if self.kill_timer % 7 == 0:
                self.image = self.death_sprites[self.kill_timer // 7]

            self.kill_timer += 1

    def shot(self, x, y):
        speed = 5
        if self.rotation == 2:
            speed = -5
        EnemyPiu(enemy_piu_group, x, y, speed)


class EnemyPiu(pygame.sprite.Sprite):
    def __init__(self, group, x, y, speed):
        super().__init__(all_sprites, group)

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, RED_HAT, (10, 10), 10)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def update(self, *args, **kwargs):
        self.rect.x -= self.speed
        if self.rect.x < 50:
            self.kill()


class HealthRunningEnemy(RunningEnemy):
    def __init__(self, group, y, rotation):
        super().__init__(group, y, rotation)

        self.image = load_image(f'heart_{rotation}.png')
        self.rect = self.image.get_rect()

        self.rect.y = y

        if rotation == 0:
            self.rect.x = 500
            self.speed = -5
        else:
            self.rect.x = 0
            self.speed = 5

    def update(self, *args, **kwargs):
        self.rect.x += self.speed
        group = args[0]
        if self.rect.x < 0 or self.rect.x > 500:
            self.kill()


class AddPatronsPiu(EnemyPiu):
    def __init__(self, group, x, y, speed):
        super().__init__(group, x, y, speed)

        pygame.draw.circle(self.image, MINT, (10, 10), 10)


# class Portal(pygame.sprite.Sprite):
#     def __init__(self, group, x, y, rotation):
#
#         super().__init__(group, all_sprites)
#
#         self.image = load_image('portal.png')
#
#         self.rect = self.image.get_rect()
#
#         self.rect.x = x
#         self.rect.y = y
#
#
#     def update(self, *args, **kwargs):


