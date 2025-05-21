import pygame
import random
from utils import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        platform_image = pygame.image.load('for pictures/Terrain/platforms.png').convert_alpha()
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #move platform side to side
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        #change platform direction
        if self.move_counter >= 100 or self.rect.left< 0 or self.rect.right > WIDTH:
            self.direction *= -1
            self.move_counter = 0

        #update platforms vert position
        self.rect.y += scroll

        #platform is gone of screen
        if self.rect.top > HEIGHT:
            self.kill()