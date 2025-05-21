import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, WIDTH, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)
        #define variables
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        animation_steps = 8
        for frame in range(animation_steps):
            image = sprite_sheet.get_image(frame, 64, 64, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            self.animation_list.append(image)


        #select started image and create rectangle
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = WIDTH
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, scroll, WIDTH, player_rect):
        #update animation
        ANIMATION_COOLDOWN = 75
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        if distance < 200:  # например, 300 пикселей — зона видимости
            self.rect.x += dx * self.direction
            self.rect.y += dy * self.direction

            self.flip = dx < 0
            self.image = pygame.transform.flip(self.image, self.flip, False)
        #move enemy
        #self.rect.x += self.direction * 2
        self.rect.y += scroll

        #chack if gone off screen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
