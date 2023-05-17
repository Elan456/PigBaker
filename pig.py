from entity import Entity
import pygame
import random
import math
import copy
import time

PIG_IMAGE = pygame.image.load("images/pig.png")
GHOST_PIG_IMAGE = pygame.image.load("images/ghost_pig.png")
BLOOD_PIG_IMAGE = pygame.image.load("images/blood_pig.png")

CALM_SOUND = pygame.mixer.Sound("sounds/calm_pig.mp3")
DYING_SOUND = pygame.mixer.Sound("sounds/pig_dying.mp3")
BOOM_SOUND = pygame.mixer.Sound("sounds/boom.wav")

print("Pig Sounds loaded")

PIG_SPEED = 1

pig_burning = False  # Used as a global variable to check if any pig is burning


class Pig(Entity):
    def __init__(self, environment):
        image = PIG_IMAGE
        x = random.randint(1500, 4000)
        y = random.randint(240, 480)
        super().__init__(x, y, image, environment)
        self.d = None
        self.held = False

        self.calm_sound = CALM_SOUND
        self.dying_sound = DYING_SOUND
        self.started_playing_audio = time.time() - 1000

        self.new_graze_direction()
        self.dead_time = None

    def new_graze_direction(self):
        self.d = random.uniform(0, math.pi * 2)

    def change_direction(self):
        self.d += random.uniform(-math.pi / 4, math.pi / 4)

    def die(self):
        self.calm_sound.stop()
        self.dying_sound.play()
        self.image = pygame.transform.rotate(self.image, 180)
        self.xv = 0
        self.yv = 0
        self.held = False
        self.dead_time = time.time()

    def update(self):
        global pig_burning
        if self.dead_time is not None:
            # We are dead
            pig_burning = True
            self.dying_sound.set_volume(1 - (abs(self.x - self.environment.player.x) / 1000))
            if time.time() - self.dead_time > self.dying_sound.get_length():
                self.active = False
                self.environment.player.pigs_killed += 1
                # Spawning a new pig and a new ghost pig
                self.environment.entities.append(Pig(self.environment))
                self.environment.entities.append(GhostPig(self.environment))
            return

        if random.randint(0, 100) == 0:
            self.change_direction()
            # Playing audio noises
            if time.time() - self.started_playing_audio > self.calm_sound.get_length():
                self.calm_sound.play(fade_ms=100)
                self.started_playing_audio = time.time()

        self.calm_sound.set_volume(1 - (abs(self.x - self.environment.player.x) / 1000))

        self.xv = math.cos(self.d) * PIG_SPEED
        self.yv = math.sin(self.d) * PIG_SPEED

        self.x += self.xv
        self.y += self.yv
        if self.collide():
            self.change_direction()

        if not self.held:
            self.held_height = 0
            if abs(self.x - 400) < 10:
                if self.x < 400:
                    self.x = 390
                    self.d = math.pi
                else:
                    self.x = 410
                    self.d = 0
        else:
            self.held_height = self.environment.player.image.get_height()


class GhostPig(Entity):
    """
    If the player gets too close, the ghost pig will chase them
    """

    def __init__(self, environment):
        x = random.randint(500, 4000)
        y = random.randint(240, 480)
        image = GHOST_PIG_IMAGE
        super().__init__(x, y, image, environment)

        self.d = 0
        self.pursuing = False

    def change_direction(self):
        self.d += random.uniform(-math.pi / 4, math.pi / 4)

    def update(self):
        """
        Wanders like a normal pig unless it gets close to the player
        """

        self.xv = math.cos(self.d) * PIG_SPEED
        self.yv = math.sin(self.d) * PIG_SPEED

        self.x += self.xv
        self.y += self.yv

        rx = self.x + self.image.get_width() / 2
        ry = self.y + self.image.get_height() / 2

        px = self.environment.player.x + self.environment.player.image.get_width() / 2
        py = self.environment.player.y + self.environment.player.image.get_height() / 2

        if self.pursuing:
            self.d = math.atan2(py - ry, px - rx)

        if self.collide() or random.randint(0, 10) == 0:
            self.change_direction()

        distance_sq = (rx - px) ** 2 + (ry - py) ** 2
        if distance_sq < 30000:
            self.pursuing = True
            if distance_sq < 1000:
                self.environment.player.drop()
                self.environment.player.x = 100
                self.x = random.randint(1000, 4000)

        if distance_sq > 60000:
            self.pursuing = False


class BloodPig(Entity):
    def __init__(self, environment):
        image = BLOOD_PIG_IMAGE
        x = 4000
        y = 0
        super().__init__(x, y, image, environment)

        self.boom_timer = time.time()
        self.boom_sound = BOOM_SOUND

    def update(self):
        self.x -= 1
        dis = abs(self.x - self.environment.player.x)
        self.boom_sound.set_volume(1 - (dis / 4000))
        if time.time() - self.boom_timer > 3:
            self.boom_sound.play()
            self.environment.camera_x += 200 * (1 - (dis / 4000)) * random.choice([-1, 1])
            self.boom_timer = time.time()
