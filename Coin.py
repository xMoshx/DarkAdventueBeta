import os
import random
import math
import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coin_list = ['assets/gold_coin_image/' + image for image in os.listdir('assets/gold_coin_image')]
        self.index = 0
        self.image = pygame.image.load(self.coin_list[self.index])
        self.level = random.randint(300, 400)
        self.speed = 5.5
        self.rect = self.image.get_rect(midbottom=(1380, self.level))

    def delete(self):  # check on main if x <= -100 and check for collision
        if self.rect.x <= -100:
            self.kill()

    def animation(self):
        self.image = pygame.image.load(self.coin_list[int(self.index)])
        self.index += 0.15
        if self.index >= len(self.coin_list):
            self.index = 0

    def update(self, score):
        if self.speed <= 20 and score > 0:
            self.speed += 0.005 * math.log(score)
        self.rect.x -= self.speed
        self.animation()
        self.delete()

