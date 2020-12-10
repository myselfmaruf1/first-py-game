# importing libraries
import pygame
import random
import math
from pygame import mixer
import time

# initialize pygame
pygame.init()

# set the screen
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("My Game")
icon = pygame.image.load('icon.svg')
pygame.display.set_icon(icon)

# Background Image
background = pygame.image.load('background2.jpeg')

# music, sounds
mixer.music.load('back.mp3')
mixer.music.play(-1)
enemyY_change_sound = mixer.Sound('enemyY_change.wav')
bullet_sound = mixer.Sound('enemyY_change.wav')
crash_sound = mixer.Sound('explosion.wav')

# fonts
font = pygame.font.Font('font3.ttf', 50)
over_font = pygame.font.Font('font1.ttf', 100)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 250, 480
bulletX_Change, bulletY_change = 0, 2
bullet_state = "steady"

# Player
playerImg = pygame.image.load('player.png')
playerX, playerY = 370, 480
playerX_change = 0

# multiple enemy appending on screen
enemyImg = []
enemyX, enemyY = [], []
enemyX_change, enemyY_change = [], []
n_enemy = 10
for i in range(n_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 720))
    enemyY.append(random.randint(0, 120))
    enemyX_change.append(0.5)
    enemyY_change.append(45)

# score count
score_val = 0  # global value for changing


# Functions
# score render
def show_score():
    score = font.render("score: " + str(score_val), True, (0, 255, 255))
    screen.blit(score, (345, 225))


# Checking Collision
def isCollision(bulletx, bullety, enemyx, enemyy):
    d = math.sqrt(pow((enemyx - bulletx), 2) + pow((enemyy - bullety), 2))
    if d < 31:
        return True
    else:
        return False


# player showing
def player(x, y):
    screen.blit(playerImg, (x, y))


# enemy showing
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# firing
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 25, y + 10))


# game over text show
def get_over_text():
    over = over_font.render("game over", True, (255, 0, 0))
    screen.blit(over, (300, 300))


# Game Loop
running = True
while running:

    for event in pygame.event.get():
        # quit on close keystroke
        if event.type == pygame.QUIT:
            print("Game is quit")
            running = False

        # key controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and enemyY[i] != 2000:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT and enemyY[i] != 2000:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "steady" and enemyY[i] != 2000:
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    screen.blit(background, (0, 0))  # background image rendering

    # Player Movement
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 735:
        playerX = 735

    # multiple enemy movement
    for i in range(n_enemy):
        # game over
        if enemyY[i] > 450:
            for j in range(n_enemy):
                enemyY[j] = 2000
            if enemyX[i] == 2000:
                crash_sound.play()
                time.sleep(5)
            get_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 730:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -0.6
        elif enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 0.6

        # collision checking
        collision = isCollision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            bulletY = 480
            bullet_state = "steady"
            score_val += 1
            print(score_val)
            enemyX[i], enemyY[i] = random.randint(0, 720), random.randint(0, 120)

        enemy(enemyX[i], enemyY[i], i)  # enemy calling

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "steady"
    if bullet_state == "fire":  # reloading bullet
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # screen update
    player(playerX, playerY)
    show_score()
    pygame.display.update()
