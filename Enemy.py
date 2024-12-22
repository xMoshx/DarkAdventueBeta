import os
import random
import math

import pygame

GROUND_LEVEL = 600

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'ground':
            self.type = 'ground'
            self.walk_list = ['assets/ground_enemy_model/' + name for name in os.listdir('assets/ground_enemy_model')]
            self.walk_index = 0
            self.image = pygame.image.load(self.walk_list[self.walk_index])
            self.level = GROUND_LEVEL + 6
            self.speed = 6
            self.gravity = 0
        else:
            self.type = 'sky'
            self.walk_list = ['assets/sky_enemy_model/' + name for name in os.listdir('assets/sky_enemy_model')]
            self.walk_index = 0
            self.image = pygame.image.load(self.walk_list[self.walk_index])
            self.level = GROUND_LEVEL - random.uniform(210, 240)
            self.speed = 6
            self.gravity = 0
            self.flight_rate = random.uniform(1, 3)
            self.flight_shift = random.uniform(-20, 2)

        self.rect = self.image.get_rect(midbottom=(1380, self.level))

    def apply_gravity(self):
        if self.type == 'ground':
            self.gravity += 0.5
            self.rect.bottom += self.gravity
            if self.rect.bottom >= GROUND_LEVEL + 6:
                self.rect.bottom = GROUND_LEVEL + 6
                self.gravity = 0

    def delete(self):
        if self.rect.x <= -100:
            self.kill()

    def animation(self):
        self.image = pygame.image.load(self.walk_list[int(self.walk_index)])
        self.walk_index += 0.1
        if self.walk_index >= len(self.walk_list):
            self.walk_index = 0

    def update(self, score):
        if self.speed <= 20 and score > 0:
            self.speed += 0.005 * math.log(score)
        self.rect.x -= self.speed
        self.apply_gravity()
        self.animation()
        self.delete()
