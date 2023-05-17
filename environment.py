import random
import time

import pygame
import entity
import pig
from pig import Pig, GhostPig, BloodPig
from death_rain import DeathRain
from player import Player

BLACK = (0, 0, 0)

BLOCK_SPACE = 200
outside_img = pygame.image.load("images/outside.png")

static_sound = pygame.mixer.Sound("sounds/static.wav")

TREE_COUNT = 20
PIG_COUNT = 1
font = pygame.font.SysFont("Arial", 30)


class Environment:
    def __init__(self, screen):
        print("environment init called")
        self.screen = screen
        self.entities = []

        self.oven = entity.Decor(60, 110, entity.oven_img, self)
        self.death_rain = DeathRain(self)
        self.entities.append(self.oven)

        self.pig_god = None
        self.pig_god_timer = None

        x = 400
        for _ in range(TREE_COUNT):
            x += random.randint(100, 400)
            self.entities.append(entity.Tree(x, self))

        for _ in range(PIG_COUNT):
            self.entities.append(Pig(self))

        self.player = Player(50, 240, self)
        self.entities.append(self.player)

        # self.gravity = 0.5

        self.camera_x = 0
        self.done = False
        self.done_time = None

    def draw(self):
        self.camera_x += (self.player.x - self.camera_x - 320) / 10

        if self.camera_x < 0:
            self.camera_x = 0
        elif self.camera_x + 640 > 3999:
            self.camera_x = 3999 - 640

        # If half of the pig god is on the screen, the game should end
        if self.pig_god is not None:
            if self.pig_god.x - self.camera_x < 320:
                if not self.done:
                    self.done = True
                    self.done_time = time.time()
                    pygame.mixer.stop()
                    static_sound.play()
                    pygame.mixer.music.stop()

                if time.time() - self.done_time > static_sound.get_length():
                    pygame.quit()
                    quit()

                self.player.x = 4000
                self.screen.fill(BLACK)
                text = font.render("Pig Baker", True, (255, 255, 255))
                self.screen.blit(text, (320 - text.get_width() / 2, 240 - text.get_height() / 2))
                return

        self.screen.blit(outside_img, (0 - self.camera_x, 0))

        # Sorting the entities by y value

        self.entities = [e for e in self.entities if e.active]
        self.entities.sort(key=lambda x: x.y + x.image.get_height() + x.held_height)
        pig.pig_burning = False
        for e in self.entities:
            e.update()
            e.draw()

        if pig.pig_burning:
            # Pause the music
            pygame.mixer.music.pause()
        else:
            # Unpause the music
            pygame.mixer.music.unpause()

        self.death_rain.update()

        if self.player.pigs_killed == 5 and self.pig_god_timer is None:
            self.death_rain.severity = 0
            # Removing all the ghost pigs and pigs
            self.entities = [e for e in self.entities if not (isinstance(e, GhostPig) or isinstance(e, Pig))]
            self.pig_god_timer = time.time()
            # Start the angry music
            pygame.mixer.music.load("sounds/angry.mp3")
            pygame.mixer.music.play(-1)

        if self.pig_god_timer is not None:
            t = time.time() - self.pig_god_timer
            self.player.pigs_killed = int(6 - (t / (20 / 5)))
            if t > 20:
                # Fade out the music
                pygame.mixer.music.fadeout(8000)
                self.pig_god_timer = None
                self.pig_god = BloodPig(self)
                self.entities.append(self.pig_god)
