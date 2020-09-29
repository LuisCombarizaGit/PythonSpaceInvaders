import pygame
pygame.font.init()
import os
import time
import random

WIDTH, HEIGHT = 750,750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders")


# Load Enemy graphics
RED_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_blue_small.png"))

# Load player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("pixel_ship_yellow.png"))

# Load laser
RED_LASER = pygame.image.load(os.path.join("pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("background-black.png")), (WIDTH, HEIGHT))




def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans",50)
    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {level}", 1, (255,100,0))
        level_label = main_font.render(f"Level: {level}", 1, (0,0,0))

        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        pygame.display.update()

    while run:
        clock.tick(FPS)  # Clock tick will be se to 60FPS
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False

main()