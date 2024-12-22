import pygame

from Enemy import Enemy
from Coin import Coin
import sys
from Player import Player
from random import randint
import math

# essentials for the game

FPS = 60
WIDTH, HEIGHT = 1280, 720
GROUND_LEVEL = 600
MAIN_FONT_SIZE = 70
LOW_FONT_SIZE = 50

# game state

game_active = False

# fonts for the game

pygame.init()

main_font = pygame.font.Font('assets/pixelletters-font/Pixellettersfull-BnJ5.ttf', MAIN_FONT_SIZE)
main_font_bg = pygame.font.Font('assets/pixelletters-font/Pixellettersfull-BnJ5.ttf', MAIN_FONT_SIZE + 3)
low_font = pygame.font.Font('assets/pixelletters-font/Pixellettersfull-BnJ5.ttf', LOW_FONT_SIZE)

# score
pygame.font.init()
score = 0
start_time = 0
score_flag = True
new_highscore = False

coins_added = 0

# initialization of screen and clock

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dark Adventure")
clock = pygame.time.Clock()

# music

pygame.mixer.music.load('assets/music/main_theme.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0, 10)
coin_sound = pygame.mixer.Sound('assets/music/coin_sound.mp3')
splat_sound = pygame.mixer.Sound('assets/music/splat-sound.mp3')

# new background stuff

scroll = 0

bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"assets/background_image/plx-{i}.png").convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    bg_images.append(bg_image)

ground_image = pygame.image.load("assets/background_image/ground.png").convert_alpha()
ground_image = pygame.transform.scale(ground_image, (600, 130))
bg_width = bg_images[0].get_width()
ground_width = ground_image.get_width()

scroll_positions = [0] * len(bg_images)

def draw_bg(score):
    for i, image in enumerate(bg_images):
        speed = 1 * (i + 1) + 0.005 * math.log(score + 0.00001)
        scroll_positions[i] = (scroll_positions[i] + speed) % bg_width
        for x in range(-1, math.ceil((WIDTH / bg_width) + 2)):
            pos_x = x * bg_width - scroll_positions[i]
            screen.blit(image, (pos_x, 0))
        speed += 0.2

def draw_solid_bg():
    for image in bg_images:
        screen.blit(image, (0, 0))

def draw_ground():
    for i in range(0, 7):
        for x in range(-1, math.ceil(WIDTH / ground_width) + 2):
            pos_x = x * ground_width - scroll
            screen.blit(ground_image, (pos_x, GROUND_LEVEL))

# Player


player = pygame.sprite.GroupSingle()
player.add(Player())


# Enemies

enemies_group = pygame.sprite.Group()


# Coins

coins_group = pygame.sprite.Group()

# ---CUSTOM EVENTS---

# enemy spawn timer

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, randint(1100, 1400))

# ground enemies timer

ground_movement_event = pygame.USEREVENT + 2
pygame.time.set_timer(ground_movement_event, randint(3000, 5000))

# coin spawn timer

coin_spawn_event = pygame.USEREVENT + 6
pygame.time.set_timer(coin_spawn_event, randint(1000, 2000))

# hero animations timers

idle_player_event = pygame.USEREVENT + 3
pygame.time.set_timer(idle_player_event, 600)

run_player_event = pygame.USEREVENT + 4
pygame.time.set_timer(run_player_event, 70)

jump_player_event = pygame.USEREVENT + 5
pygame.time.set_timer(jump_player_event, 270)
# functions
def spawn_enemies(enemies_group):
    enemy_type = 'ground'
    if randint(0, 200) % 2:
        enemy_type = 'sky'
    enemies_group.add(Enemy(enemy_type))


def sky_enemies_movement(enemies_group):
    for enemy in enemies_group:
        if enemy.type == 'sky':
            enemy.rect.y += math.sin((enemy.rect.x / 100.0) + enemy.flight_shift) * enemy.flight_rate


def ground_enemies_movement(enemies_group):
    for enemy in enemies_group:
        if enemy.type == 'ground' and not randint(0, 200) % 2:
            enemy.gravity -= 14
            if enemy.rect.y < GROUND_LEVEL:
                break


def spawn_coins(coins_group):
    if randint(0, 200) % 3 == 0:
        coins_group.add(Coin())


def collision():
    if pygame.sprite.spritecollide(player.sprite, enemies_group, False):
        if pygame.sprite.spritecollide(player.sprite, enemies_group, False, pygame.sprite.collide_mask):
            splat_sound.play()
            enemies_group.empty()
            return False
    return True


def coin_collision(coins_added):
    if pygame.sprite.spritecollide(player.sprite, coins_group, False):
        if pygame.sprite.spritecollide(player.sprite, coins_group, True, pygame.sprite.collide_mask):
            coin_sound.play()
            return coins_added + 5
    return coins_added


def draw_score(screen, score):
    score_surf = low_font.render(f"score: {score}", False, '0x141921')
    score_rect = score_surf.get_rect(center=(100, 80))
    screen.blit(score_surf, score_rect)


def set_high_score(file_path, new_score):
    with open(file_path, 'r') as f:
        score = f.read()
        if not score:
            with open(file_path, 'w') as f:
                f.write(str(new_score))
            return True
        elif int(score) < new_score:
            with open(file_path, 'w') as f:
                f.write(str(new_score))
            return True
        return False

def get_high_score(file_path):
    with open(file_path, 'r') as f:
        score = f.read()
        if not score:
            return 0
        return score


# game loop

while True:
    keys = pygame.key.get_pressed()
    score = (pygame.time.get_ticks() - start_time) // 1000 + coins_added

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == enemy_timer and game_active:
            spawn_enemies(enemies_group)

        if event.type == coin_spawn_event and game_active:
            spawn_coins(coins_group)

        if event.type == ground_movement_event and game_active:
            ground_enemies_movement(enemies_group)

        if not game_active:
            player.sprite.image = pygame.image.load(player.sprite.idle_list[player.sprite.idle_counter]).convert_alpha()
            if event.type == idle_player_event:
                player.sprite.image = pygame.image.load(
                    player.sprite.idle_list[player.sprite.idle_counter]).convert_alpha()
                player.sprite.idle_counter = (player.sprite.idle_counter + 1) % len(player.sprite.idle_list)

        if event.type == run_player_event and game_active and player.sprite.rect.bottom >= GROUND_LEVEL:
            player.sprite.image = pygame.image.load(player.sprite.run_list[player.sprite.run_counter]).convert_alpha()
            player.sprite.jump_counter = 0
            player.sprite.run_counter = (player.sprite.run_counter + 1) % len(player.sprite.run_list)
            if keys[pygame.K_LEFT]:
                player.sprite.image = pygame.transform.flip(player.sprite.image, 180, 0).convert_alpha()

        if event.type == jump_player_event and player.sprite.rect.bottom < GROUND_LEVEL and game_active:
            player.sprite.image = pygame.image.load(player.sprite.jump_list[player.sprite.jump_counter]).convert_alpha()
            player.sprite.jump_counter = (player.sprite.jump_counter + 1) % len(player.sprite.jump_list)

    if game_active:

        scroll = (scroll + 5) % ground_width
        draw_bg(score)
        draw_ground()

        player.draw(screen)
        player.update()

        if keys[pygame.K_RIGHT]:
            for i in range(len(scroll_positions)):
                scroll_positions[i] += 0.5
            scroll += 0.5
            for enemy in enemies_group:
                enemy.speed = 6.5
            for coin in coins_group:
                coin.speed = 6

        if keys[pygame.K_LEFT]:
            for i in range(len(scroll_positions)):
                scroll_positions[i] -= 0.5
            scroll -= 0.5
            for enemy in enemies_group:
                enemy.speed = 5.5
            for coin in coins_group:
                coin.speed = 5

        enemies_group.draw(screen)
        enemies_group.update(score)

        sky_enemies_movement(enemies_group)

        coins_group.draw(screen)
        coins_group.update(score)

        coins_added = coin_collision(coins_added)

        # collision with enemies

        game_active = collision()

        # score record
        draw_score(screen, score)

    # game ain't active

    else:
        draw_solid_bg()
        draw_ground()
        screen.blit(player.sprite.image, (500, 320))

        coins_group.empty()

        new_highscore_surf = main_font.render("NEW Highscore. Good job!", False, "0xfcf162")


        if score_flag:
            new_highscore = set_high_score('highscore.txt', score)
            score_flag = False
        if new_highscore:
            screen.blit(new_highscore_surf, (325, 200))
        highscore_surf = main_font.render(f"HIGHSCORE: {get_high_score('highscore.txt')}", False, '0x141921')
        start_game_surf = main_font.render("Press SPACE to start your Dark Adventure...", False, '0x141921')
        screen.blit(highscore_surf, (450, 300))
        screen.blit(start_game_surf, (100, 100))

        if keys[pygame.K_SPACE]:
            player.sprite.kill()
            player.add(Player())
            player.sprite.rect.x = 80
            player.draw(screen)
            game_active = True
            score_flag = True
            start_time = pygame.time.get_ticks()
            coins_added = 0

    pygame.display.update()
    clock.tick(FPS)
  
