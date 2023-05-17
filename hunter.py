from entity import Entity
import pygame


class Hunter(Entity):
    """
    Can move and shoot
    The player will be a hunter that goes for the pigs
    Other Hunters may compete with the player for pigs or even shoot the player
    """

    def __init__(self, x, y, image, environment):
        super().__init__(x, y, image, environment)

        self.pigs_killed = 0
        self.held_pig = None

    def update(self):
        """
        Updates x and y values based on xv and yv
        Brings the hunter down based on gravity
        """

        self.x += self.xv
        self.y += self.yv

        self.xv *= 0.8  # Friction
        self.yv *= 0.8  # Friction

        self.collide()

        if self.held_pig is not None:
            self.held_pig.x = self.x + self.image.get_width() / 2 - self.held_pig.image.get_width() / 2
            self.held_pig.y = self.y - self.held_pig.image.get_height()

    def drop(self):
        if self.held_pig is not None:
            self.held_pig.held = False
            self.held_pig = None

    def try_pig_pickup(self):
        if self.held_pig is not None:
            # Check if we are putting it in the oven
            # If we brought the pig to the oven, then kill it
            if abs(self.x - self.environment.oven.x) < 200 and self.y > self.environment.oven.y + 100:
                self.held_pig.die()
                self.held_pig = None
                self.environment.death_rain.severity += .05
                return

            self.held_pig.y += self.image.get_height()
            self.held_pig.held = False
            self.held_pig = None
            return

        for e in self.environment.entities:
            if e != self and e.__class__.__name__ == "Pig" and e.dead_time is None:
                if self.x + self.image.get_width() > e.x and self.x < e.x + e.image.get_width():
                    if self.y + self.image.get_height() > e.y and self.y < e.y + e.image.get_height():
                        self.held_pig = e
                        e.held = True
