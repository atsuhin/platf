import pygame
import os

WIDTH, HEIGHT= 400, 700
FPS = 60
PLAYER_SPEED = 10
GRAVITY = 1
MAX_PLATFORMS = 10
SCROLL_THRESH = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_text(text, font, text_color, x, y, screen):
    image = font.render(text, True, text_color)
    screen.blit(image, (x, y))

def draw_panel(score, font_small, screen):
    draw_text('Score: ' + str(score), font_small, BLACK, 0, 0, screen)

def draw_background(bg_scroll, screen, back_image):
    screen.blit(back_image, (0, 0 + bg_scroll))
    screen.blit(back_image, (0, -700 + bg_scroll))

def load_high_score():
    if os.path.exists('score.txt'):
        with open('score.txt', 'r') as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open('score.txt', 'w') as file:
        file.write(str(score))