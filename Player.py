import pygame
import os

GROUND_LEVEL = 600
WIDTH, HEIGHT = 1280, 720


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_counter = 0
        self.idle_list = ['assets/player_model/Idle/idle1.png', 'assets/player_model/Idle/idle2.png']
        self.run_counter = 0
        self.run_list = ['assets/player_model/run/' + name for name in os.listdir('assets/player_model/run')]
        self.jump_counter = 0
        self.jump_list = ['assets/player_model/jump/' + name for name in os.listdir('assets/player_model/jump')]
        self.image = pygame.image.load(self.run_list[self.run_counter])
        self.rect = self.image.get_rect(midbottom=(200, GROUND_LEVEL))
        self.gravity = 0
        self.speed = 6
        self.mask = pygame.mask.from_surface(self.image)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= GROUND_LEVEL:
            self.gravity -= 26
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_DOWN]:
            self.gravity += 1.5

    def boundaries(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.boundaries()
