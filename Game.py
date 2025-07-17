import pygame
import Point
import Spline
import numpy as np

def draw_spline(screen, spline, color=(255, 255, 255), resolution=100):
    points = []
    for i in range(resolution + 1):
        t = i / resolution
        pt = spline.get_point(t)
        points.append((int(pt.x), int(pt.y)))
    pygame.draw.lines(screen, color, False, points, 2)

WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Demo")
clock = pygame.time.Clock()

p1 = Point.Point(100, 300, h=0)
p2 = Point.Point(700, 500, h=0)

s = Spline.Spline(p1, p2)

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_spline(screen, s, color=(0, 255, 0), resolution=200)

    pygame.draw.circle(screen, (255, 0, 0), (int(p1.x), int(p1.y)), 6)
    pygame.draw.circle(screen, (0, 0, 255), (int(p2.x), int(p2.y)), 6)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()