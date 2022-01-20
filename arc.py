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
t = pygame.font.SysFont('Century Gothic', 40, bold=False)
bl = [pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50) for i in range(7) for j in range(4)]
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
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over == False and win == False:
            start, play = False, True

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
        pygame.draw.rect(dis, pygame.Color('black'), pl)
        pygame.draw.circle(dis, pygame.Color('red'), sh.center, R)

    t_life = t.render(f'Life: {life}', 1, pygame.Color('white'))
    dis.blit(t_life, (15, 5))
    t_score = t.render(f'Score: {score}/{ko}', 1, pygame.Color('white'))
    dis.blit(t_score, (160, 5))
    if game_over == True:
        t_gameover = t.render('Game over!', 1, pygame.Color('RED'))
        dis.blit(t_gameover, (500, 400))
    elif win:
        t_win = t.render('You win!', 1, pygame.Color('Blue'))
        dis.blit(t_win, (500, 400))

    pygame.display.flip()
    vre.tick(60)
