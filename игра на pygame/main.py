import pygame
import os
import random 
from spritessheet import SpriteSheet
from enemy import Enemy
from pygame import mixer
from platform_1 import Platform
from shooter import Bullet
mixer.init()
pygame.init()

WIDTH, HEIGHT= 400, 700
FPS = 60
PLAYER_SPEED = 10
GRAVITY = 1
MAX_PLATFORMS = 10
SCROLL_THRESH = 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
score = 0

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else: 
    high_score = 0


screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Jumper")

back_image = pygame.image.load('for pictures/back_ground/background.png').convert_alpha()
character_image = pygame.image.load('for pictures/MainCharacter/idle.png').convert_alpha()
platform_image = pygame.image.load('for pictures/Terrain/platforms.png').convert_alpha()
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 25)
dragon_sheet_img = pygame.image.load('for pictures/Enemy/dragon enemy.png').convert_alpha()
dragon_sheet = SpriteSheet(dragon_sheet_img)
pygame.mixer.music.load('sounds/Sneaky-Snitch(chosic.com).mp3')
pygame.mixer.music.play(-1, 0.0)



def draw_text(text, font, text_color, x, y):
    image = font.render(text, True, text_color)
    screen.blit(image, (x, y))

#
def draw_panal():
    draw_text('Score: ' + str(score), font_small, BLACK, 0, 0)

#for drawinf
def draw_background(bg_scroll):
    screen.blit(back_image, (0, 0 + bg_scroll))
    screen.blit(back_image, (0, -700 + bg_scroll))

class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(character_image, (55, 55))
        self.width = 42
        self.height = 52
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.val_y = 0
        self.flip = False


    def move(self):
        #reset variables
        dx = 0
        dy = 0
        scroll = 0

        #keypress
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx -= PLAYER_SPEED
            self.flip = True
        if key[pygame.K_d]:
            dx = PLAYER_SPEED
            self.flip = False

        #gravity
        self.val_y += GRAVITY
        dy += self.val_y

        #if player out of screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right

        #chaeck with platforms
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #checking above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.val_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.val_y = -20
                    
        

        #chack if player bounced to the top
        if self.rect.top <= SCROLL_THRESH:
            #if jumping
            if self.val_y < 0:
                scroll = -dy

        #update position
        self.rect.x += dx
        self.rect.y += dy + scroll

        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self, ):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10, self.rect.y - 5))


    
#instances
character = Player(WIDTH // 2, HEIGHT - 150)

platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


def main(screen):
    clock = pygame.time.Clock()
    scroll = 0
    bg_scroll = 0
    game_over = False
    fade_counter = 0
    global score, high_score

    #start platform
    platform = Platform(WIDTH // 2 - 25, HEIGHT - 100, 50, False)
    platform_group.add(platform)
    

     
    running = True
    while running:
        
        clock.tick(FPS)
        if game_over == False:
            scroll = character.move()
            
            #draw bacground
            bg_scroll += scroll
            if bg_scroll >=700:
                bg_scroll = 0
            draw_background(bg_scroll)

            #generate platforms
            if len(platform_group) < MAX_PLATFORMS:
                p_w = random.randint(40, 60)
                p_x = random.randint(0, WIDTH - p_w)
                p_y = platform.rect.y - random.randint(80, 120)
                p_type = random.randint(1, 2)
                if p_type == 1 and score > 500:
                    p_moving = True
                else:
                    p_moving = False
                platform = Platform(p_x, p_y, p_w, p_moving)
                platform_group.add(platform)

            #update platforms
            platform_group.update(scroll)

            #generate enemies
            if len(enemy_group) == 0 and score > 500:
                enemy = Enemy(WIDTH, 100, dragon_sheet, 1.5)
                enemy_group.add(enemy)

            #updete enemies
            enemy_group.update(scroll, WIDTH, character.rect)

            for bullet in bullet_group:
                hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True, pygame.sprite.collide_mask)
                if hit_enemies:
                    bullet.kill()

            bullet_group.update()

            #update score 
            if scroll > 0:
                score += scroll

            #draw line at pre
            pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), 
                             (WIDTH, score - high_score + SCROLL_THRESH), 3)
            draw_text('high score', font_small, WHITE, WIDTH - 130, score - high_score + SCROLL_THRESH)
            
           
            bullet_group.draw(screen)

            #draw sprites
            platform_group.draw(screen)
            enemy_group.draw(screen)
            character.draw()

            #draw panal
            draw_panal()

            #check game over
            if character.rect.top > HEIGHT:
                game_over = True
            #check for enemies
            if pygame.sprite.spritecollide(character, enemy_group, False):
                if pygame.sprite.spritecollide(character, enemy_group, False, pygame.sprite.collide_mask):
                    game_over = True
        else:
            if fade_counter < WIDTH:
                fade_counter += 5
                pygame.draw.rect(screen, BLACK, (0, 0, fade_counter, HEIGHT) )
            else:
                draw_text('GAME OVER', font_big, WHITE, 40, 200)
                draw_text('SCORE: ' + str(score), font_big, WHITE, 40, 250)
                draw_text('Press space to restart', font_big, WHITE, 40, 300)

                #update high_score
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))

                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    game_over = False
                    score = 0
                    scroll = 0
                    fade_counter = 0

                    #reposition character
                    character.rect.center = (WIDTH // 2, HEIGHT - 150)
                    #reset enemies
                    enemy_group.empty()
                    #reset platform
                    platform_group.empty()
                    platform = Platform(WIDTH // 2 - 25, HEIGHT - 100, 50, False)
                    platform_group.add(platform)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #update high_score
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка
                mouse_pos = pygame.mouse.get_pos()
                bullet = Bullet(character.rect.centerx, character.rect.centery, mouse_pos)
                bullet_group.add(bullet)
        pygame.display.update()

    pygame.quit()   
    quit() 

            
if __name__ == "__main__":
    main(screen)