# Template - szablon
import pygame
import random
import sys
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

##Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "spine_rifle.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.y_speed = 5

    def update(self, *args):
        self.rect.x +=5
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT:
            self.y_speed = -5
        if self.rect.top < 0:
            self.y_speed = 5
        if self.rect.left > WIDTH:
            self.rect.right = 0


# #Mierzenie czasu
# delta = 0.0
# delta+=clock.tick() / 1000.0

##inicjalizacja
pygame.init()
#Dźwięk
pygame.mixer.init()
#Tworzenie obrazu
screen = pygame.display.set_mode((WIDTH,HEIGHT))
#Nazwa okna
pygame.display.set_caption("Nazwa gry")
#Zegar do ogarniania fps
clock = pygame.time.Clock()
#Sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

##Loop (input,update,render)
running = True
while running:
    #loop right speed
    clock.tick(FPS)


    #Events,input,process
    for event in pygame.event.get():
        #check for closing windows
        if event.type == pygame.QUIT:
            running = False

    ##Update
    all_sprites.update()

    ##Draw/Render
    screen.fill(BLUE)
    all_sprites.draw(screen)
    #after drawing everything!!!!! flip and display
    pygame.display.flip()

pygame.quit()