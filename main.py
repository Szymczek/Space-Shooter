# Space Mission - Survive!
# Art by https://agresko.itch.io/
# Dodaj strzelanie ciągłe w buffach, downgrade dodaj, Tlo wejsciowe, dodatkowe zycia, dodac tarcze, wrogów w szyku
# Zmienic grafike, dzwiek strzelnia, dodac animacje strzalu, zamienic grafike, dodac animacje do pojazdu
# Popraw Ekspolzje - grafika
import pygame
import random
from os import path

# Folders----
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Config
WIDTH = 480
HEIGHT = 800
FPS = 60
OBJECTS = 10
POWERUP_TIME = 5000
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# init/sound/screen/time/font
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Mission - Survive!")
clock = pygame.time.Clock()
font_name = pygame.font.get_default_font()


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Space Mission - Survive!", 36, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Move 'w,a,s,d', Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 10, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_sur = font.render(text, True, WHITE)
    text_rect = text_sur.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_sur, text_rect)


def draw_shield(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 15
    fill = (pct * bar_length) / 100
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, RED, outline_rect)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 40 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def newmob():
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_org = random.choice(astroid_img)
        self.image = self.image_org.copy()
        self.image_org.set_colorkey(BLACK)
        self.rect = self.image_org.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = random.randrange(-100, -70)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 4)
        self.rot = 0
        self.rot_speed = random.randrange(-6, 6)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_org, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self, *args):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT or self.rect.right > WIDTH + 150 or self.rect.left < -150 or self.rect.y < -150:
            self.rect.x = random.randrange(WIDTH)
            self.rect.y = random.randrange(-70, -40)
            self.speedy = random.randrange(1, 10)
            self.speedx = random.randrange(-3, 4)


class BgElement(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, random.randrange(3, 60)))
        self.image.fill(WHITE)
        self.image.set_alpha(75)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - 50)
        self.rect.y = random.randrange(-300, -140)
        self.speedy = random.randrange(10, 20)

    def update(self, *args):
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT:
            self.rect.x = random.randrange(0, WIDTH - 50)
            self.rect.y = random.randrange(-300, -40)
            self.speedy = random.randrange(10, 20)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (80, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 37
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 10
        self.speedy = 10
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_deley = 250
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self, *args):
        # timeout
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()
        # hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT - 10)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_d]:
            self.rect.x += self.speedx
        if keystate[pygame.K_a]:
            self.rect.x -= self.speedx
        if keystate[pygame.K_w]:
            self.rect.y -= self.speedy
        if keystate[pygame.K_s]:
            self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if keystate[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_deley:
            self.last_shoot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.y)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.right, self.rect.y)
                bullet2 = Bullet(self.rect.left, self.rect.y)
                all_sprites.add(bullet1, bullet2)
                bullets.add(bullet1, bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet = Bullet(self.rect.centerx, self.rect.y)
                bullet1 = Bullet(self.rect.right, self.rect.y)
                bullet2 = Bullet(self.rect.left, self.rect.y)
                all_sprites.add(bullet, bullet1, bullet2)
                bullets.add(bullet, bullet1, bullet2)
                shoot_sound.play()

    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (12, 36))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.now = pygame.time.get_ticks()

    def update(self, *args):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = pygame.transform.scale(powerups_images[self.type], (45, 45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 0

    def update(self, *args):
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.kill()


# Load all Graphics
background = pygame.image.load(path.join(img_dir, 'bacground_selfmade.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'sprite_3.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (30, 30))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'laser_p.png')).convert()
astroid_img = []
astroid_list = ['astroid.png', 'astroid_1.png', 'astroid_2.png', 'astroid_3.png', 'astroid_4.png']
for img in astroid_list:
    astroid_img.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
explosion_anim["player"] = []
for element in range(0, 30):
    filename = pygame.image.load(path.join(img_dir, "1_{}.png".format(element)))
    img = filename.convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (200, 200))
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (64, 64))
    explosion_anim["sm"].append(img_sm)
for i in range(1, 7):
    filename = pygame.image.load(path.join(img_dir, "Explosion_{}.png".format(i)))
    img = filename.convert()
    img.set_colorkey(WHITE)
    img_pl = pygame.transform.scale(img, (100, 100))
    explosion_anim["player"].append(img_pl)
powerups_images = {}
powerups_images['shield'] = pygame.image.load(path.join(img_dir, 'PurpleCoin.png')).convert()
powerups_images['gun'] = pygame.image.load(path.join(img_dir, 'GoldCoin5.png')).convert()

# Load all Sounds
power_shield = pygame.mixer.Sound(path.join(snd_dir, "Powerup_1.wav"))
power_gun = pygame.mixer.Sound(path.join(snd_dir, "Powerup_2.wav"))
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser.wav'))
explosion_snd = []
explosion_sounds = ['Explosion.wav', 'Explosion_2.wav']
for snd in explosion_sounds:
    explosion_snd.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_death_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion_p.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'Orbital Colossus.mp3'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

# Loop (input,update,render)
running = True
game_over = True
while running:
    if game_over:
        show_go_screen()
        score = 0
        # Sprites
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        powerups = pygame.sprite.Group()
        for i in range(20):
            green_square = BgElement()
            all_sprites.add(green_square)
        for i in range(OBJECTS):
            newmob()
            green_square = BgElement()
            all_sprites.add(green_square)
        game_over = False

    # Loop right speed
    clock.tick(FPS)
    # Events,input,process
    for event in pygame.event.get():
        # check for closing windows
        if event.type == pygame.QUIT:
            running = False

    # Kolizje, dodano circle collide
    hits_p_m = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)  # list
    for hit in hits_p_m:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield < 0:
            player_death_sound.play()
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1
            if player.lives == 0:
                player.kill()
            player.shield = 100
    # if the player died and the explosion has ended
    if player.lives == 0 and not death_expl.alive():
        game_over = True
    hits_m_b = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits_m_b:
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        score += 50 - hit.radius
        newmob()
        random.choice(explosion_snd).play()
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
    hits_m_p = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits_m_p:
        if hit.type == "shield":
            power_shield.play()
            player.shield += random.randrange(20, 60)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "gun":
            power_gun.play()
            player.powerup()

    # Update
    all_sprites.update()
    mobs.update()
    # Draw/Render
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    mobs.draw(screen)
    draw_text(screen, "Score: " + str(score), 25, WIDTH / 2, 10)
    draw_shield(screen, 10, 10, player.shield)
    draw_lives(screen, WIDTH - 120, 5, player.lives, player_mini_img)
    # after drawing everything!!!!! flip and display
    pygame.display.flip()

pygame.quit()
