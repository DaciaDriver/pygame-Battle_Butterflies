import pygame
import os  # for paths
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 650  # constant values in capital
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # dimensions of window
pygame.display.set_caption("Battle of Butterflyes")  # window title

WHITE = (255, 255, 255)  # RGB White
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (138, 43, 226)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit_sound.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'fire_sound.wav'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 60)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5  # velocity
BULLET_VEL = 7
MAX_BULLETS = 3  # per shoot
BUTTERFLY_WIDTH, BUTTERFLY_HEIGHT = 80, 100  # dimensions of images

BLUE_HIT = pygame.USEREVENT + 1
PURPLE_HIT = pygame.USEREVENT + 2

BUTTERFLY_BLUE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'butterfly_blue.png'))
BUTTERFLY_BLUE = pygame.transform.scale(
    BUTTERFLY_BLUE_IMAGE, (BUTTERFLY_WIDTH, BUTTERFLY_HEIGHT))

BUTTERFLY_PURPLE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'butterfly_purple.png'))
BUTTERFLY_PURPLE = pygame.transform.scale(
    BUTTERFLY_PURPLE_IMAGE, (BUTTERFLY_WIDTH, BUTTERFLY_HEIGHT))

BACKGROUD = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'landscape.jpg')), (WIDTH, HEIGHT))


def draw_window(blue, purple, blue_bullets, purple_bullets, blue_health, purple_health):  # update game
    WIN.blit(BACKGROUD, (0, 0))
    # WIN.fill(WHITE)  # fill the background
    pygame.draw.rect(WIN, BLACK, BORDER)

    blue_health = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    purple_health = HEALTH_FONT.render(
        "Health: " + str(purple_health), 1, WHITE)
    WIN.blit(blue_health, (WIDTH - blue_health.get_width() - 10, 10))
    WIN.blit(purple_health, (10, 10))

    # pygame starts coordonates on left top corner
    WIN.blit(BUTTERFLY_BLUE, (blue.x, blue.y))
    WIN.blit(BUTTERFLY_PURPLE, (purple.x, purple.y))

    for bullet in purple_bullets:
        pygame.draw.rect(WIN, PURPLE, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()


def blue_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL + 20 > 0:  # left
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width - 20 < BORDER.x:  # right
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL + 20 > 0:  # up
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height - 20 < HEIGHT:  # down
        blue.y += VEL


def purple_movement(keys_pressed, purple):
    if keys_pressed[pygame.K_LEFT] and purple.x - VEL > BORDER.x + BORDER.width:  # left
        purple.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and purple.x + VEL + purple.width < WIDTH:  # right
        purple.x += VEL
    if keys_pressed[pygame.K_UP] and purple.y - VEL > 0:  # up
        purple.y -= VEL
    if keys_pressed[pygame.K_DOWN] and purple.y + VEL + purple.height < HEIGHT:  # down
        purple.y += VEL


def handle_bullets(blue_bullets, purple_bullets, blue, purple):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if purple.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PURPLE_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)

    for bullet in purple_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            purple_bullets.remove(bullet)
        elif bullet.x < 0:
            purple_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2,
             HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():
    blue = pygame.Rect(100, 300, BUTTERFLY_WIDTH, BUTTERFLY_HEIGHT)
    purple = pygame.Rect(700, 300, BUTTERFLY_WIDTH, BUTTERFLY_HEIGHT)

    blue_bullets = []
    purple_bullets = []

    blue_health = 10
    purple_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # control the speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit window
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:  # shooting
                if event.key == pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(purple_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        purple.x, purple.y + purple.height//2 - 2, 10, 5)
                    purple_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == BLUE_HIT:
                purple_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == PURPLE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()

        winner = ""
        if blue_health <= 0:
            winner = "Blue Butterfly Wins!"

        if purple_health <= 0:
            winner = "Purple Butterfly Wins!"

        if winner != "":
            draw_winner(winner)
            break

        keys_pressed = pygame.key.get_pressed()
        blue_movement(keys_pressed, blue)
        purple_movement(keys_pressed, purple)

        handle_bullets(blue_bullets, purple_bullets, blue, purple)

        draw_window(blue, purple, blue_bullets,
                    purple_bullets, blue_health, purple_health)

    # pygame.quit()
    main()


if __name__ == "__main__":
    main()
