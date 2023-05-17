import pygame
from hunter import Hunter

PLAYER_IMG = pygame.image.load("images/player.png")


class Player(Hunter):
    """
    Controlled by the player to move and shoot, collecting pigs for points
    """

    def __init__(self, x, y, environment):
        image = PLAYER_IMG
        super().__init__(x, y, image, environment)

        self.pigs_killed = 0

    def control(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.xv += -1
        elif keys_pressed[pygame.K_RIGHT]:
            self.xv += 1

        if keys_pressed[pygame.K_UP]:
            self.yv -= 1
        elif keys_pressed[pygame.K_DOWN]:
            self.yv += 1
