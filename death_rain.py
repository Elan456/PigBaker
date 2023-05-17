"""
A poison rain starts after the first pig is killed
If the rain hits the player, the player dies
"""

import pygame

from entity import Entity
import random
import math

RAIN_DROP_IMAGE = pygame.image.load("images/raindrop.png")


class DeathRain:
    def __init__(self, environment):
        self.environment = environment
        self.severity = 0
        self.spawn_count = 0

    def update(self):
        self.spawn_count += self.severity
        if self.spawn_count >= 1:
            for i in range(int(self.spawn_count)):
                self.environment.entities.append(RainDrop(self.environment))
            self.spawn_count -= int(self.spawn_count)



class RainDrop(Entity):
    def __init__(self, environment):
        x = random.randint(400, 4000)
        y = -100
        image = RAIN_DROP_IMAGE
        super().__init__(x, y, image, environment)

    def update(self):
        if self.y < 480:
            self.y += 5
        else:
            self.active = False

        # Checking if we hit the player
        if abs(self.x + self.image.get_width() / 2 - (self.environment.player.x + self.environment.player.image.get_width() / 2)) < 30:
            if abs(self.y + self.image.get_height() / 2 - (self.environment.player.y + self.environment.player.image.get_height() / 2)) < 30:
                self.environment.player.drop()
                self.environment.player.x = 100

