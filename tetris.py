import pygame
from copy import deepcopy
from random import choice, randrange

weight, height = 10, 16
t = 45
GAME_RES = weight * t, height * t
FPS = 60
RES = 864, 800

pygame.init()
screen = pygame.display.set_mode(RES)
game_screen = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

g = [pygame.Rect(x * t, y * t, t, t) for x in range(weight) for y in range(height)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
figures = [[pygame.Rect(x + weight // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, t - 2, t - 2)
f = [[0 for i in range(weight)] for j in range(height)]

a_count, a_speed, a_limit = 0, 60, 2000

bg1 = pygame.image.load('data/background.png').convert()
bg = pygame.transform.scale(bg1, (864, 800))


font = pygame.font.Font('font/font.ttf', 45)
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('red'))


get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if figure[i].x < 0 or figure[i].x > weight - 1:
        return False
    elif figure[i].y > height - 1 or f[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    record = get_record()
    dx, rotate = 0, False
    screen.blit(bg, (0, 0))
    screen.blit(game_screen, (20, 20))

    for i in range(lines):
        pygame.time.wait(200)


    game_screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                a_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True

    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    a_count += a_speed
    if a_count > a_limit:
        a_count = 0
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    f[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                a_limit = 2000
                break

    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break


    line, lines = height - 1, 0
    for row in range(height - 1, -1, -1):
        count = 0
        for i in range(weight):
            if f[row][i]:
                count += 1
            f[line][i] = f[row][i]
        if count < weight:
            line -= 1
        else:
            a_speed += 3
            lines += 1

    score += scores[lines]


    [pygame.draw.rect(game_screen, (40, 40, 40), i_rect, 1) for i_rect in g]
    for i in range(4):
        figure_rect.x = figure[i].x * t
        figure_rect.y = figure[i].y * t
        pygame.draw.rect(game_screen, color, figure_rect)

    for y, raw in enumerate(f):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * t, y * t
                pygame.draw.rect(game_screen, col, figure_rect)

    for i in range(4):
        figure_rect.x = next_figure[i].x * t + 380
        figure_rect.y = next_figure[i].y * t + 185
        pygame.draw.rect(screen, next_color, figure_rect)


    screen.blit(title_score, (520, 380))
    screen.blit(font.render(str(score), True, pygame.Color('black')), (520, 430))
    screen.blit(title_record, (520, 520))
    screen.blit(font.render(record, True, pygame.Color('gold')), (520, 570))


    for i in range(weight):
        if f[0][i]:
            set_record(record, score)
            f = [[0 for i in range(weight)] for i in range(height)]
            a_count, a_speed, a_limit = 0, 60, 2000
            score = 0
            for i_rect in g:
                pygame.draw.rect(game_screen, get_color(), i_rect)
                screen.blit(game_screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
