import pygame
import math
from utils import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

        # Рассчёт направления к мышке
        direction_x = target_pos[0] - x
        direction_y = target_pos[1] - y
        length = (direction_x**2 + direction_y**2) ** 0.5
        if length == 0:
            length = 1
        self.velocity_x = (direction_x / length) * 15
        self.velocity_y = (direction_y / length) * 15

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Удаление, если пуля вышла за экран
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()