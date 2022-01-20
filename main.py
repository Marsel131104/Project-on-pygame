import pygame
import random

pygame.init()

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
bg = pygame.transform.scale(bg1, (864, 688))
bg3 = pygame.image.load('data/background-night.png')
bg2 = pygame.transform.scale(bg3, (864, 688))
bg_first = pygame.image.load('data/message.png')
#bg_first = pygame.transform.scale(bg4, (864, 688))
ground_image1 = pygame.image.load('data/base.png')
ground_image = pygame.transform.scale(ground_image1, (880, 112))
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

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

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
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                import menu
    pygame.display.update()
pygame.quit()
