# Template - szablon
import pygame
import random
import sys

WIDTH = 480
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# #Mierzenie czasu
# delta = 0.0
# delta+=clock.tick() / 1000.0

# inicjalizacja
pygame.init()
# Dźwięk
pygame.mixer.init()
# Tworzenie obrazu
screen = pygame.display.set_mode((WIDTH,HEIGHT))
# Nazwa okna
pygame.display.set_caption("Nazwa gry")
# Zegar do ogarniania fps
clock = pygame.time.Clock()
# Sprites
all_sprites = pygame.sprite.Group()


# Loop (input,update,render)
running = True
while running:
    # Loop right speed
    clock.tick(FPS)

    # Events,input,process
    for event in pygame.event.get():
        # check for closing windows
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw/Render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # after drawing everything!!!!! flip and display
    pygame.display.flip()

pygame.quit()
