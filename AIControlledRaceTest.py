import pygame
import Racer
import TrackManager
import numpy as np
import RacingEnv
from stable_baselines3 import SAC

env = RacingEnv.RacingEnv()
model = SAC.load("racer_model")

WIDTH, HEIGHT = 800, 600
compass_size = 100
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Demo")
clock = pygame.time.Clock()

running = True

track = TrackManager.TrackManager()
racer = Racer.Racer()

throttle = 0
turn = 0

while running:
    dt = clock.tick(FPS) / 1000  # Not used yet
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    
    obs = env.get_observation_from_state(racer, track, throttle, turn)
    action, _ = model.predict(obs)

    throttle = float(action[0])
    turn = float(action[1])

    racer.update(throttle, turn)
    track.update(racer.delta)

    racer.draw(screen)
    track.draw(screen)

    pygame.draw.line(screen, (200, 200, 200), (WIDTH - 2.0*compass_size, HEIGHT - compass_size), (WIDTH, HEIGHT - compass_size), 10)
    pygame.draw.line(screen, (200, 200, 200), (WIDTH - compass_size, HEIGHT - 2.0*compass_size), (WIDTH - compass_size, HEIGHT), 10)
    pygame.draw.line(screen, (255, 0, 0), (WIDTH - compass_size, HEIGHT - compass_size), (WIDTH - compass_size, HEIGHT - compass_size + compass_size*throttle), 5)
    pygame.draw.line(screen, (255, 0, 0), (WIDTH - compass_size, HEIGHT - compass_size), (WIDTH - compass_size + compass_size*turn, HEIGHT - compass_size), 5)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()