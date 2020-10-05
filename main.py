import pygame
pygame.font.init()
import os
import time
import random

WIDTH, HEIGHT = 650, 650
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

class Laser:
    def __init__(self,x,y,image):
        self.x_position = x
        self.y_position = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self,window):
        window.blit(self.image, (self.x_position,self.y_position))

    def move(self,vel):
        self.y_position += vel

    def off_screen(self,height):
        return not self.y_position <= height and self.y_position >= 0

    def collision(self, obj):
        return collide(obj, self)


# Abstract class I will use to inherent all other s
class Ship():
    COOLDOWN = 30
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
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

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

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)


    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                     (self.x_position, self.y_position + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
        self.x_position, self.y_position + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))


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

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x_position, self.y_position, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1,obj2):
    offset_x = obj2.x_position - obj1.x_position
    offset_y = obj2.y_position - obj1.y_position
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None

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

    player = Player(290, 500)
    lost = False
    lost_count = 0
    laser_vel = 5

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
        redraw_window()

        if lives <= 0 or player.health <=0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

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
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_speed)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0,2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y_position + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


main()