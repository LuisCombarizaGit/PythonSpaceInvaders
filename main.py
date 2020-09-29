import pygame
import os
import time
import random

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
BG = pygame.image.load(os.path.join("background-black.png"))


