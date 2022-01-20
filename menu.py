import pygame
import pygame_menu
import random


def flappy_bird():
    clock = pygame.time.Clock()
    fps = 60

    screen_width = 864
    screen_height = 800

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Flappy Bird')

    font = pygame.font.SysFont('Bauhaus 93', 60)

    white = (255, 255, 255)
    max_score = 0
    ground_scroll = 0
    scroll_speed = 4
    flying = False
    game_over = False
    pipe_gap = 150
    pipe_freqency = 1500
    last_pipe = pygame.time.get_ticks() - pipe_freqency
    score = 0
    pass_pipe = False
    bg1 = pygame.image.load('data/background-day.png')
    bg = pygame.transform.scale(bg1, (900, 688))
    bg3 = pygame.image.load('data/background-night.png')
    bg2 = pygame.transform.scale(bg3, (900, 688))
    bg_first = pygame.image.load('data/message.png')
    # bg_first = pygame.transform.scale(bg4, (864, 688))
    ground_image1 = pygame.image.load('data/base.png')
    ground_image = pygame.transform.scale(ground_image1, (915, 112))
    button_img = pygame.image.load('data/gameover.png')
    n = 0

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def reset_game():
        pipe_group.empty()
        flappy.rect.x = 100
        flappy.rect.y = int(screen_height / 2)
        score = 0
        scroll_speed = 4
        return scroll_speed, score

    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 4):
                img = pygame.image.load(f'data/bird{num}.png')
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.vel = 0
            self.clicked = False

        def update(self):
            if flying:
                self.vel += 0.5
                if self.vel > 8:
                    self.vel = 8
                if self.rect.bottom < 684:
                    self.rect.y += int(self.vel)
            if not game_over:
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    self.vel = -10
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

                self.counter += 1
                flap_cooldown = 5
                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                self.image = self.images[self.index]

                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2.5)
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90)

    class Pipe(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
            pygame.sprite.Sprite.__init__(self)
            image1 = pygame.image.load('data/pipe-green.png')
            self.image = pygame.transform.scale(image1, (52, 550))
            self.rect = self.image.get_rect()
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
            if position == -1:
                self.rect.topleft = [x, y + int(pipe_gap / 2)]

        def update(self):
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()

    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self):
            action = False
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    action = True

            screen.blit(self.image, (self.rect.x, self.rect.y))
            return action

    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()
    flappy = Bird(80, int(screen_height / 2))
    bird_group.add(flappy)

    button = Button(screen_width // 2 - 70, screen_height // 2 - 50, button_img)

    running = True
    while running:
        clock.tick(fps)
        if max_score <= score:
            max_score = score
        if not flying and not game_over:
            screen.blit(bg, (0, 0))
            screen.blit(bg_first, (340, 270))
        else:
            screen.blit(bg, (0, 0))
            if score >= 10:
                screen.blit(bg2, (0, 0))
        if score % 10 == 0 and score != 0:
            scroll_speed += 0.01

        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)

        screen.blit(ground_image, (ground_scroll, 688))

        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and not pass_pipe:
                pass_pipe = True
            if pass_pipe:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str('Score: ' + str(score)), font, white, 10, 10)
        draw_text(str('Max: ' + str(max_score)), font, white, 10, 50)

        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True

        if flappy.rect.bottom >= 683:
            game_over = True
            flying = False

        if not game_over and flying:

            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_freqency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 60:
                ground_scroll = 0
            pipe_group.update()
        if game_over:
            if button.draw():
                game_over = False
                scroll_speed = reset_game()[0]
                score = reset_game()[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ''
        pygame.display.update()
    pygame.quit()


def arcanoidd():
    from random import randrange as rnd
    import pygame

    pygame.init()

    def work(kx, ky, ball, rect):
        if kx > 0:
            dx = ball.right - rect.left
        else:
            dx = rect.right - ball.left
        if ky > 0:
            dy = ball.bottom - rect.top
        else:
            dy = rect.bottom - ball.top

        if (dx - dy) < 5:
            kx, ky == -kx, -ky
        if dx > dy:
            ky *= -1
        if dy > dx:
            kx *= -1

        return kx, ky

    width, height = 864, 800
    dis = pygame.display.set_mode((width, height))
    vre = pygame.time.Clock()
    img = pygame.image.load('data/1.jpg').convert()
    t = pygame.font.SysFont('Arial Black', 40, bold=False)
    bl = [pygame.Rect(10 + 120 * i, 60 + 70 * j, 100, 50) for i in range(7) for j in range(4)]
    c_bl = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(7) for j in range(4)]
    score, ko = 0, len(bl)

    pl = pygame.Rect(150, 530, 100, 20)

    R = 12
    sh = pygame.Rect(190, 510, R, R)
    cv, cb, life = 1, -1, 3

    start, play, game_over, win = True, False, False, False

    while True:
        dis.blit(img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game_over == False and win == False:
                start, play = False, True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ''

        if game_over == False and win == False:
            key = pygame.key.get_pressed()
            if key[pygame.K_d] and pl.right < width:
                pl.x += 10

                if start:
                    sh.x += 10
            if key[pygame.K_a] and pl.left > 0:
                pl.x -= 10

                if start == True:
                    sh.x -= 10

        if play == True:
            sh.x += 4 * cv
            sh.y += 4 * cb

            if sh.x < R or sh.x > width - R:
                cv *= -1
            if sh.y - 50 < R:
                cb *= -1

            if sh.colliderect(pl) and cb > 0:
                cv, cb = work(cv, cb, sh, pl)

            yni = sh.collidelist(bl)
            if yni != -1:
                yni_rect = bl.pop(yni)

                cv, cb = work(cv, cb, sh, yni_rect)

                score += 1

            if sh.y > height + R:
                play, start = False, True

                pl.x, pl.y = 150, 530
                sh.x, sh.y = 190, 510

                life -= 1

                if life <= 0:
                    game_over = True

            if score == ko:
                play, win = False, True

        pygame.draw.aaline(dis, pygame.Color('black'), [0, 50], [width, 50])
        [pygame.draw.rect(dis, c_bl[color], i) for color, i in enumerate(bl)]

        if game_over == False:
            pygame.draw.rect(dis, pygame.Color('white'), pl)
            pygame.draw.circle(dis, pygame.Color('purple'), sh.center, R)

        t_life = t.render(f'Life: {life}', 1, pygame.Color('white'))
        dis.blit(t_life, (15, 5))
        t_score = t.render(f'Score: {score}/{ko}', 1, pygame.Color('white'))
        dis.blit(t_score, (580, 5))
        if game_over == True:
            t_gameover = t.render('Game over!', 1, pygame.Color('RED'))
            dis.blit(t_gameover, (320, 400))
        elif win:
            t_win = t.render('You win!', 1, pygame.Color('GREEN'))
            dis.blit(t_win, (350, 400))

        pygame.display.flip()
        vre.tick(60)


def tetisok():
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
                elif event.key == pygame.K_ESCAPE:
                    return ''
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


def menushka():
    pygame.init()
    surface = pygame.display.set_mode((864, 800))
    menu = pygame_menu.Menu('Select game', 864, 800, theme=pygame_menu.themes.THEME_GREEN)
    menu.add.text_input('Name :', default='Player')
    menu.add.button('Flappy bird', flappy_bird)
    menu.add.button('Arkanoid', arcanoidd)
    menu.add.button('Tetris', tetisok)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)


while True:
    menushka()
