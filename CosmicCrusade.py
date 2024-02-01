import pygame
import sys
import math
import random
from pygame.locals import *
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((540, 768))
background = pygame.image.load('space.jpg')
mixer.music.load("background.wav")

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

playerImg = pygame.image.load('player.png')
playerX = 250
playerY = 680
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyImg.append(pygame.image.load('enemy1.png'))
    enemyX.append(random.randint(0, 480))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(20)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 680
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def set_background():
    global background
    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    '''image'''

def move_bullet():
    global bulletX, bulletY, bullet_state
    if bulletY <= 0:
        bulletY = 680
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

def key_bindings():
    global running, playerX_change, bulletX, playerX, bulletY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 480:
        playerX = 480


def MoveEnemies():
    global enemyX, enemyX_change, enemyY, enemyY_change
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 20:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 480:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)


def collision():
    global num_of_enemies, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value, playerX, playerY
    for i in range(num_of_enemies):
        player_collision = isCollision(playerX, playerY, enemyX[i], enemyY[i])
        if player_collision:
            PlayerExplodionSound = mixer.Sound("explosion.wav")
            PlayerExplodionSound.play()
            game_over_text = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(game_over_text, (180, 384))
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            sys.exit()

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 480)
            enemyY[i] = random.randint(50, 150)

running = True
while running:
    set_background()
    key_bindings()
    MoveEnemies()
    collision()
    move_bullet()
    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()