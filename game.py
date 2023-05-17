import pygame
pygame.font.init()
pygame.mixer.init()
from player import Player
from environment import Environment
from hunter import Hunter
import time

pygame.init()


pygame.display.set_caption("Pig Baker")
pygame.display.set_icon(pygame.image.load("images/icon.png"))

screen = pygame.display.set_mode((640, 480))

# Being playing the ambient music on an infinite loop
pygame.mixer.music.load("sounds/ambient_music.mp3")
font = pygame.font.SysFont("Arial", 25)


def play():
    clock = pygame.time.Clock()
    environment = Environment(screen)
    intro_time = time.time()
    while time.time() - intro_time < 5:
        # Give the player a chance to read the instructions
        # Putting words on a black background, spooky font
        screen.fill((0, 0, 0))
        text = font.render("If I burn five, it\'ll come.", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()

    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    environment.player.try_pig_pickup()

        keys_pressed = pygame.key.get_pressed()
        environment.player.control(keys_pressed)
        environment.draw()

        pygame.draw.rect(screen, (100, 100, 100), [0, 0, 120, 20])

        # For every pig killed, put a circle in the top left
        for i in range(environment.player.pigs_killed):
            pygame.draw.circle(screen, (255, 0, 0), (i * 25 + 10, 10), 10)

        pygame.display.update()
        clock.tick(60)

        screen.fill((255, 255, 255))
