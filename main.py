import pygame

from game_play import game_play

from constants import SIZE, PLATINUM, RED, GREY

from objects import load_image


def main():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    running = True

    font_for_game_title = pygame.font.Font('data/fonts/FlappyBirdRegular.ttf', 140)

    press_any_font = pygame.font.Font('data/fonts/FlappyBirdRegular.ttf', 40)

    game_name = font_for_game_title.render('HAPPY BIRD', True, RED)
    press_any_text = press_any_font.render('PRESS ANY KEY TO START', True, GREY)

    pygame.display.set_icon(load_image('bird/2.png'))
    pygame.display.set_caption('happy bird')

    while running:
        screen.fill(PLATINUM)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                game_play()

        screen.blit(game_name, (250 - (game_name.get_size()[0] // 2), 150))
        screen.blit(press_any_text, (250 - (press_any_text.get_size()[0] // 2), 270))
        pygame.display.flip()


if __name__ == '__main__':
    main()