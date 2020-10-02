import pygame
pygame.font.init()
import os
import time
import random

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load Enemy graphics
RED_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_blue_small.png"))

# Load player 
YELLOW_SPACE_ = pygame.image.load(os.path.join("pixel_ship_yellow.png"))

# Load laser
RED_LASER = pygame.image.load(os.path.join("pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("background-black.png")), (WIDTH, HEIGHT))

# Abstract class I will use to inherent all other s
class Ship():
    def __init__(self, x_position, y_position, health = 100):
        self.x_position = x_position
        self.y_position = y_position
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x_position, self.y_position))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

# player 
class Player(Ship):
    def __init__(self, x_position, y_position, health = 100):
        super().__init__(x_position, y_position, health)
        self.ship_img = YELLOW_SPACE_
        self.lasers_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    def __init__(self,x_position, y_position,color, health = 100):
        super().__init__(x_position,y_position,health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,speed):
        self.y_position += speed

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 70)

    enemies = []
    wave_length = 5
    enemy_speed = 2

    player_speed = 5

    player = Player(300, 650)
    lost = False

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))  # Take an image and make it into the surface background
        # draw lives and level into game
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 100, 0))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        # Position of labels
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        player.draw(WIN)
        for j in enemies:
            j.draw(WIN)

        if lost:
            lost_label = lost_font.render("YOU LOST",1,(255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)  # Clock tick will be se to 60FPS

        if lives <= 0 or player.health <=0:
            lost = True

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(100, WIDTH - 100), random.randrange(-1500, -10),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False

        # Check which keys are pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x_position - player_speed > 0:  # move left
            player.x_position -= player_speed
        if keys[pygame.K_d] and player.x_position + player_speed + player.get_width() < WIDTH : # move right
            player.x_position += player_speed
        if keys[pygame.K_w] and player.y_position - player_speed > 0:  # move up
            player.y_position -= player_speed
        if keys[pygame.K_s] and player.y_position + player_speed + player.get_height() < HEIGHT: # move down
            player.y_position += player_speed

        for enemy in enemies[:]:
            enemy.move(enemy_speed)
            if enemy.y_position + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()

main()