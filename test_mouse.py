# Template - szablon
import pygame
import random
import sys
import math

WIDTH = 1280
HEIGHT = 720
FPS = 120

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# class Blocks(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface((50, 50))
#         self.image.fill(GREEN)
#         self.rect = self.image.get_rect()
#         self.dot = pygame.mouse.get_rel()
#         self.rect.center = (WIDTH / 2, HEIGHT - 40)
#
#     def update(self):
#         pass
#
#     def shoot(self):
#         pass
#         # bullet = Bullet()
#         # all_sprites.add(bullet)
#         # bullets.add(bullet)

    # def rotate(self):
    #     mouse_x , mouse_y=pygame.mouse.get_pos()
    #     rel_x , rel_y = mouse_x - self.rect.x , mouse_y - self.rect.y
    #     angle = (180 / math.pi) * -math.atan2(rel_y , rel_x)
    #     self.image = pygame.transform.rotate(self.image , int(angle))
    #     self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        pos_m = pygame.mouse.get_pos()
        self.rect.x = pos_m[0]
        self.rect.y = pos_m[1]

    def update(self):
        pass
        # self.rect.x = pos_m[0]
        # self.rect.y = pos_m[1]


# inicjalizacja
pygame.init()
pygame.mixer.init()
# Tworzenie obrazu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nazwa gry")
clock = pygame.time.Clock()
# Sprites
all_sprites = pygame.sprite.Group ()
bullets = pygame.sprite.Group()
# Tworzenie obiektu
# blocks = Blocks()
bullet = Bullet()
# Dodawanie obiektów
# all_sprites.add(bullet)


# Koniec

# Loop (input,update,render)
running = True
while running:
    keystate=pygame.key.get_pressed()
    # Loop right speed
    clock.tick(FPS)
    pos_m=pygame.mouse.get_pos()

    # Events,input,process
    for event in pygame.event.get():
        # check for closing windows
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets.add(bullet)
            all_sprites.add(bullet)

    # Update
    all_sprites.update()
    # Draw/Render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # after drawing everything!!!!! flip and display
    pygame.display.flip()

pygame.quit()
