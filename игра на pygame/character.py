import pygame

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

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10, self.rect.y - 5))

