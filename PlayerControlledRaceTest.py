import pygame
import Racer
import TrackManager
import numpy as np

WIDTH, HEIGHT = 800, 600
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
    fwd = 0
    rot = 0
    if keys[pygame.K_UP]:
        fwd += 1
    if keys[pygame.K_DOWN]:
        fwd -= 1
    if keys[pygame.K_LEFT]:
        rot -= 1
    if keys[pygame.K_RIGHT]:
        rot += 1
    
    throttle += np.sign(fwd-throttle)*min(abs(fwd-throttle),10*dt)
    turn += np.sign(rot-turn)*min(abs(rot-turn),5*dt)

    racer.update(throttle, turn)
    track.update(racer.delta)

    racer.draw(screen)
    track.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()