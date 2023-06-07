import pygame
import time
import random
import sys

snake_speed = 15
snake_color = (0, 255, 0)
fruit_color = (255, 255, 255)
window_color = (0, 0, 0)
error_color = (255, 0, 0)
text_color = (200, 200, 200)

window_x = 720
window_y = 480

pygame.init()
font = pygame.font.Font(None, 36)

win = pygame.display.set_mode((window_x, window_y))

snake_position = [100, 50]

snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

fruit_position = [random.randrange(1, window_x // 10) * 10, random.randrange(1, window_y // 10) * 10]
fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

difficulty = {'ЛЕГКО': 10, 'СРЕДНЕ': 25, 'ТЯЖЕЛО': 40}
level = 'СРЕДНЕ'

pause = False


def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Твои очки : ' + str(score), True, error_color)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    win.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


def show_score():
    score_font = pygame.font.SysFont('times new roman', 20)
    score_surface = score_font.render('ОЧКИ : ' + str(score), True, text_color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (window_x / 10, 15)
    win.blit(score_surface, score_rect)


def game():
    global pause, direction, change_to, score, fruit_position, fruit_spawn, snake_body, snake_position

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pause = not pause

        if pause:
            pause_menu()
            continue

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, window_x // 10) * 10, random.randrange(1, window_y // 10) * 10]

        fruit_spawn = True
        win.fill(window_color)

        for pos in snake_body:
            pygame.draw.rect(win, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(win, fruit_color, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        show_score()

        pygame.display.update()

        clock = pygame.time.Clock()
        clock.tick(snake_speed)


def pause_menu():
    global pause
    continue_button = font.render('Продолжить', True, (255, 255, 255))
    continue_button_active = font.render('Продолжить', True, (255, 0, 0))
    continue_button_rect = continue_button.get_rect(center=(window_x / 2, window_y / 2))

    quit_button = font.render('Выйти', True, (255, 255, 255))
    quit_button_active = font.render('Выйти', True, (255, 0, 0))
    quit_button_rect = quit_button.get_rect(center=(window_x / 2, window_y / 2 + 50))

    menu_option = 0

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_option -= 1
                elif event.key == pygame.K_DOWN:
                    menu_option += 1
                elif event.key == pygame.K_RETURN:
                    if menu_option == 0:
                        pause = False
                    elif menu_option == 1:
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        menu_option %= 2

        win.fill((0, 0, 0))
        win.blit(continue_button_active if menu_option == 0 else continue_button, continue_button_rect)
        win.blit(quit_button_active if menu_option == 1 else quit_button, quit_button_rect)

        pygame.display.flip()


def menu():
    global snake_speed, level

    title = font.render('Игра змейка', True, (255, 255, 255))
    title_rect = title.get_rect(center=(window_x / 2, window_y / 4))

    play_game = font.render('Начать игру', True, (255, 255, 255))
    play_game_active = font.render('Начать игру', True, (255, 0, 0))
    play_game_rect = play_game.get_rect(center=(window_x / 2, window_y / 2))

    options = font.render('Настройка сложности', True, (255, 255, 255))
    options_active = font.render('Настройка сложности', True, (255, 0, 0))
    options_rect = options.get_rect(center=(window_x / 2, window_y / 2 + 50))

    quit_game = font.render('Выйти из игры', True, (255, 255, 255))
    quit_game_active = font.render('Выйти из игры', True, (255, 0, 0))
    quit_game_rect = quit_game.get_rect(center=(window_x / 2, window_y / 2 + 100))

    menu_option = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_option -= 1
                elif event.key == pygame.K_DOWN:
                    menu_option += 1
                elif event.key == pygame.K_RETURN:
                    if menu_option == 0:
                        game()
                    elif menu_option == 1:
                        options_menu()
                    elif menu_option == 2:
                        pygame.quit()
                        sys.exit()

        menu_option %= 3

        win.fill((0, 0, 0))
        win.blit(title, title_rect)
        win.blit(play_game_active if menu_option == 0 else play_game, play_game_rect)
        win.blit(options_active if menu_option == 1 else options, options_rect)
        win.blit(quit_game_active if menu_option == 2 else quit_game, quit_game_rect)

        pygame.display.flip()


def options_menu():
    global snake_speed, level

    easy_mode = font.render('ЛЕГКО', True, (255, 255, 255))
    easy_mode_active = font.render('ЛЕГКО', True, (255, 0, 0))
    easy_mode_rect = easy_mode.get_rect(center=(window_x / 2, window_y / 2 - 50))

    medium_mode = font.render('СРЕДНЕ', True, (255, 255, 255))
    medium_mode_active = font.render('СРЕДНЕ', True, (255, 0, 0))
    medium_mode_rect = medium_mode.get_rect(center=(window_x / 2, window_y / 2))

    hard_mode = font.render('ТЯЖЕЛО', True, (255, 255, 255))
    hard_mode_active = font.render('ТЯЖЕЛО', True, (255, 0, 0))
    hard_mode_rect = hard_mode.get_rect(center=(window_x / 2, window_y / 2 + 50))

    back = font.render('ВЕРНУТЬСЯ', True, (255, 255, 255))
    back_active = font.render('ВЕРНУТЬСЯ', True, (255, 0, 0))
    back_rect = back.get_rect(center=(window_x / 2, window_y / 2 + 100))

    options = [easy_mode, medium_mode, hard_mode, back]
    options_active = [easy_mode_active, medium_mode_active, hard_mode_active, back_active]
    options_rect = [easy_mode_rect, medium_mode_rect, hard_mode_rect, back_rect]

    options_option = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    options_option -= 1
                elif event.key == pygame.K_DOWN:
                    options_option += 1
                elif event.key == pygame.K_RETURN:
                    if options_option == 0:
                        level = 'ЛЕГКО'
                        snake_speed = difficulty[level]
                        return
                    elif options_option == 1:
                        level = 'СРЕДНЕ'
                        snake_speed = difficulty[level]
                        return
                    elif options_option == 2:
                        level = 'ТЯЖЕЛО'
                        snake_speed = difficulty[level]
                        return
                    elif options_option == 3:
                        return

        options_option %= 4

        win.fill((0, 0, 0))
        for i in range(4):
            win.blit(options_active[i] if options_option == i else options[i], options_rect[i])

        pygame.display.flip()


if __name__ == '__main__':
    menu()
