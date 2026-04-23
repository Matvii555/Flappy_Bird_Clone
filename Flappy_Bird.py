import pygame
from pygame import *
from random import randint

init()

# Налаштування вікна
window_size = (1200, 800)
window = display.set_mode(window_size)
display.set_caption("Flappy Bird Clone")
clock = time.Clock()

# Налаштування гравця
size = 60
player_rect = Rect(150, window_size[1] // 2, size, size)
y_vel = 0  # Швидкість падіння
gravity = 0.8
jump_power = -15


def generate_pipes(count, start_x, pipe_width=100, gap=220):
    pipes = []
    distance = 400  # Відстань між трубами
    for i in range(count):
        height = randint(100, 450)
        top_pipe = Rect(start_x + i * distance, 0, pipe_width, height)
        bottom_pipe = Rect(start_x + i * distance, height + gap, pipe_width, window_size[1])
        pipes.append(top_pipe)
        pipes.append(bottom_pipe)
    return pipes


# Початкові труби
pipes = generate_pipes(10, window_size[0])
main_font = font.Font(None, 100)
score = 0
lose = False

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        # Стрибок на пробіл або W
        if e.type == KEYDOWN:
            if (e.key == K_w or e.key == K_SPACE) and not lose:
                y_vel = jump_power
            if e.key == K_r and lose:  # Рестарт на R
                player_rect.y = window_size[1] // 2
                pipes = generate_pipes(10, window_size[0])
                score = 0
                y_vel = 0
                lose = False

    if not lose:
        # Гравітація та рух
        y_vel += gravity
        player_rect.y += y_vel

        # Рух труб
        for pipe in pipes:
            pipe.x -= 7

            # Перевірка зіткнення
            if player_rect.colliderect(pipe):
                lose = True

        # Вихід за межі екрана
        if player_rect.bottom >= window_size[1] or player_rect.top <= 0:
            lose = True

        # Видалення старих труб та додавання нових
        if pipes[0].x < -100:
            pipes.pop(0)  # Видаляємо верхню
            pipes.pop(0)  # Видаляємо нижню
            score += 1
            # Додаємо нову трубу в кінець черги
            new_pipe_x = pipes[-1].x + 400
            pipes += generate_pipes(1, new_pipe_x)

    # Малювання
    window.fill("sky blue")

    for pipe in pipes:
        draw.rect(window, "darkgreen", pipe)

    draw.rect(window, "yellow", player_rect)

    # Текст рахунку
    score_text = main_font.render(f"Score: {int(score)}", True, "black")
    window.blit(score_text, (window_size[0] // 2 - 100, 50))

    if lose:
        lose_text = main_font.render("GAME OVER! Press R", True, "red")
        window.blit(lose_text, (window_size[0] // 2 - 350, window_size[1] // 2))

    display.update()
    clock.tick(60)

quit()
