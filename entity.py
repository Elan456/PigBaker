import pygame
import random

tree_img = pygame.image.load("images/tree.png")
oven_img = pygame.image.load("images/oven.png")


class Entity:
    def __init__(self, x, y, image, environment):
        self.x = x
        self.y = y
        self.image = image
        self.height = self.image.get_height()
        self.environment = environment  # Contains all the other entities and the map

        self.xv = 0
        self.yv = 0

        self.held_height = 0
        self.on_ground = False
        self.active = True

    def update(self):
        raise NotImplementedError

    def collide(self):
        r = False
        max_height = 300
        if self.y + self.height < max_height:
            self.y = max_height - self.height
            self.yv = 0
            r = True

        if self.y + self.height > 480:
            self.y = 480 - self.height
            self.yv = 0
            r = True

        if self.x < 0:
            self.x = 0
            r = True

        elif self.x + self.image.get_width() > 4000:
            self.x = 4000 - self.image.get_width()
            r = True

        return r

    def draw(self):
        # Will use the mirrored image if facing left
        if self.xv < 0:
            self.environment.screen.blit(pygame.transform.flip(self.image, True, False),
                                         (self.x - self.environment.camera_x, self.y))
        else:
            self.environment.screen.blit(self.image, (self.x - self.environment.camera_x, self.y))


class Decor(Entity):
    def __init__(self, x, y, image, environment):
        super().__init__(x, y, image, environment)

    def update(self):
        pass


class Tree(Decor):
    def __init__(self, x, environment):
        image = tree_img
        y = random.randint(-25, 200)
        super().__init__(x, y, image, environment)
