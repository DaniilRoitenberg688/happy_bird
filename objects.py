import pygame
from random import randrange
from constants import *
from functions import *
from groups import *


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


class TubeUp(pygame.sprite.Sprite):
    def __init__(self, speed, group):
        super().__init__(group)

        self.image = pygame.Surface((50, randrange(50, 300)))

        self.rect = self.image.get_rect()

        self.image.fill(GREEN)

        self.rect.x = 500
        self.rect.y = 0

        self.speed = speed

    def update(self, *args, **kwargs):
        self.rect.x += self.speed
        if self.rect.x < -50:
            self.kill()


class TubeDown(pygame.sprite.Sprite):
    def __init__(self, speed, group, between, high_up):
        super().__init__(group)

        high = SIZE - between - high_up

        if high < 0:
            self.kill()
            return

        self.image = pygame.Surface((50, SIZE - between - high_up))

        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

        self.rect.x = 500
        self.rect.y = between + high_up

        self.speed = speed

    def update(self, *args, **kwargs):
        self.rect.x += self.speed
        if self.rect.x < -50:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        # self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # self.image = self.image.convert_alpha()
        # pygame.draw.circle(self.image, GOLD, (10, 10), 10)

        self.sprites = [load_image('spaceship.png', -1)]
        self.sprites.append(pygame.transform.rotate(self.sprites[0], 30))

        self.image = load_image('spaceship.png', -1)

        self.rect = self.image.get_rect()

        self.rect.x = 200
        self.rect.y = 250

        self.is_jump = 0

        self.patrons = 12

        self.counter = 0

        self.gravity = 5

        self.is_cheat = False

        self.hp = 3



    def update(self, *args, **kwargs):
        keys = args[0]

        if not self.is_cheat:

            if keys[pygame.K_UP]:
                self.image = self.sprites[1]
                self.is_jump = 5
                self.gravity = 4

            if self.is_jump:
                self.rect.y -= self.is_jump * 2
                self.is_jump -= 1

            if not self.is_jump:
                self.image = self.sprites[0]
                self.gravity = 5

            self.rect.y += self.gravity

        else:
            if keys[pygame.K_UP]:
                self.rect.y -= 4
            if keys[pygame.K_DOWN]:
                self.rect.y += 4

        if not self.is_cheat and (
                pygame.sprite.spritecollideany(self, tube_group) or
                pygame.sprite.spritecollideany(self, enemies_group) or
                pygame.sprite.spritecollideany(self, enemy_piu_group)):
            self.hp -= 1

    def shot(self, group):
        Piu(group=group, x=self.rect.x + 5, y=self.rect.y)
        self.patrons -= 1


class RunningEnemy(pygame.sprite.Sprite):
    def __init__(self, group, y):
        super().__init__(group)

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, PURPLE, (15, 15), 15)

        self.rect = self.image.get_rect()

        self.rect.x = 500
        self.rect.y = y

        self.speed = 5

        self.hp = 1

    def update(self, *args, **kwargs):
        self.rect.x -= self.speed
        group = args[0]
        if self.rect.x < 0:
            self.kill()

        if pygame.sprite.spritecollideany(self, group):
            self.hp -= 1

        if not self.hp:
            self.kill()


class Piu(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)

        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, GOLD, (6, 6), 6)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = 7

    def update(self, *args, **kwargs):
        self.rect.x += self.speed
        if self.rect.x > 500:
            self.kill()

        sprite = pygame.sprite.spritecollideany(self, enemies_group)
        if sprite:
            self.kill()
            sprite.hp -= 1

        enemies_piu = pygame.sprite.spritecollideany(self, enemy_piu_group)
        if enemies_piu:
            self.speed *= -1
            enemies_piu.speed *= -1
            new_piu = EnemyPiu(piu_group, enemies_piu.rect.x, enemies_piu.rect.y)
            new_piu.speed = -5
            enemies_piu.kill()


class EmptyTube(pygame.sprite.Sprite):
    def __init__(self, group, y, high, speed):
        super().__init__(group)

        self.image = pygame.Surface((50, high), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = 500
        self.rect.y = y

        self.speed = speed

    def update(self, *args, **kwargs):
        self.rect.x += self.speed
        if self.rect.x < -50:
            self.kill()


class PiuingEnemy(pygame.sprite.Sprite):
    def __init__(self, group, y):
        super().__init__(group)

        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, MUSLIM_GREEN, (20, 20), 20)

        self.rect = self.image.get_rect()

        self.rect.x = 500
        self.rect.y = y

        self.new_y = None

        self.speed = 2

        self.wait_counter = 0

        self.piu_or_not = False

        self.hp = 2

    def update(self, *args, **kwargs):
        if self.rect.x > 400:
            self.rect.x -= 3

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
                    EnemyPiu(enemy_piu_group, self.rect.x, self.rect.y + 10)
                    self.piu_or_not = True

                else:
                    self.wait_counter += 1
            else:
                if self.new_y > self.rect.y:
                    self.rect.y += self.speed
                else:
                    self.rect.y -= self.speed


class EnemyPiu(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, RED_HAT, (10, 10), 10)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = 5

    def update(self, *args, **kwargs):
        self.rect.x -= self.speed
        if self.rect.x < 50:
            self.kill()


class HealthRunningEnemy(RunningEnemy):
    def __init__(self, group, y):
        super().__init__(group, y)

        pygame.draw.circle(self.image, KING_FUCHSIA, (15, 15), 15)
