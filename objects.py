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
            self.image = pygame.Surface((50, randrange(50, 300)))

        self.rotation = rotation

        self.rect = self.image.get_rect()

        self.image.fill(GREEN)

        if self.rotation == 0:
            self.rect.x = 500
            self.rect.y = 0
            self.speed_x = speed
            self.speed_y = 0

        if self.rotation == 2:
            self.rect.x = -50
            self.rect.y = 0
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
            self.image = pygame.Surface((50, SIZE - between - high_up))

        self.image.fill(GREEN)

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

        self.sprites = [load_image(f'spaceship_{0}.png', -1), '', load_image(f'spaceship_{2}.png', -1)]

        self.image = load_image(f'spaceship_{rotation}.png', -1)

        self.rect = self.image.get_rect()

        self.rotation = rotation

        self.rect.x = 231
        self.rect.y = 250

        self.is_jump = 0

        self.patrons = 12

        self.counter = 0

        self.gravity = 5

        self.is_cheat = False

        self.hp = 3

    def update(self, *args, **kwargs):
        keys = args[0]
        rotation = args[1]
        self.rotation = rotation

        self.image = self.sprites[rotation]

        if not self.is_cheat:

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.is_jump = 5
                self.gravity = 4

            if self.is_jump:
                self.rect.y -= self.is_jump * 2
                self.is_jump -= 1

            if not self.is_jump:
                self.gravity = 5

            self.rect.y += self.gravity

        else:
            if keys[pygame.K_UP]:
                self.rect.y -= 4
            if keys[pygame.K_DOWN]:
                self.rect.y += 4

    def shot(self, group):
        Piu(group=group, x=self.rect.x + 5, y=self.rect.y, rotation=self.rotation)
        self.patrons -= 1


class RunningEnemy(pygame.sprite.Sprite):
    def __init__(self, group, y, rotation):
        super().__init__(all_sprites, group)

        self.image = load_image('asteroid.png', -1)

        self.rect = self.image.get_rect()

        self.right_image = self.image

        self.degree = 0

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
        group = args[0]
        if self.rect.x < 0 or self.rect.x > 500:
            self.kill()

        if pygame.sprite.spritecollideany(self, group):
            self.hp -= 1

        if not self.hp:
            self.kill()

        self.degree += 1
        self.image = pygame.transform.rotate(self.right_image, -self.degree)


class Piu(pygame.sprite.Sprite):
    def __init__(self, group, x, y, rotation):
        super().__init__(all_sprites, group)

        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, GOLD, (6, 6), 6)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        if rotation == 0:
            self.speed = 7

        if rotation == 2:
            self.speed = -7

    def update(self, *args, **kwargs):
        self.rect.x += self.speed
        if self.rect.x > 500 or self.speed < -50:
            self.kill()

        sprite = pygame.sprite.spritecollideany(self, enemies_group)
        if sprite:
            self.kill()
            sprite.hp -= 1

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

        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, MUSLIM_GREEN, (20, 20), 20)

        self.rect = self.image.get_rect()

        if rotation == 0:
            self.rect.x = 500
            self.rect.y = y

        if rotation == 2:
            self.rect.x = 0
            self.rect.y = y

        self.rotation = rotation

        self.new_y = None

        self.speed = 2

        self.wait_counter = 0

        self.piu_or_not = False

        self.hp = 2

    def update(self, *args, **kwargs):

        if self.rotation == 0:
            if self.rect.x > 400:
                self.rect.x -= 3

        if self.rotation == 2:
            if self.rect.x < 60:
                self.rect.x += 3

        if self.hp == 0:
            self.kill()

        if pygame.sprite.spritecollideany(self, piu_group):
            self.hp -= 1

        if self.new_y is None:
            self.new_y = randrange(50, 450)

        elif self.new_y is not None:
            if abs(self.new_y - self.rect.y) <= 5:
                if self.wait_counter == 50:
                    self.new_y = None
                    self.wait_counter = 0
                    self.piu_or_not = False

                elif self.wait_counter == 25 and not self.piu_or_not:
                    if self.rotation == 0:
                        self.shot(self.rect.x, self.rect.y + 10)

                    if self.rotation == 2:
                        self.shot(self.rect.x + 35, self.rect.y + 10)

                    self.piu_or_not = True

                else:
                    self.wait_counter += 1
            else:
                if self.new_y > self.rect.y:
                    self.rect.y += self.speed
                else:
                    self.rect.y -= self.speed

    def shot(self, x, y):
        speed = 5
        if self.rotation == 2:
            speed = -5

        if randrange(1, 101) % 3 == 0:
            AddPatronsPiu(add_patrons_group, x, y, speed)
            return
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
