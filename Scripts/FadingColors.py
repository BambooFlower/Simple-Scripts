# Fading colors animation 

import pygame
import itertools

pygame.init()

screen = pygame.display.set_mode((800, 600))

colors = itertools.cycle(['green', 'blue', 'purple', 'pink', 'red', 'orange'])

clock = pygame.time.Clock()

base_color = next(colors)
next_color = next(colors)
current_color = base_color

FPS = 60
change_every_x_seconds = 3.
number_of_steps = change_every_x_seconds * FPS
step = 1

font = pygame.font.SysFont('Arial', 50)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    text = font.render('fading {a} to {b}'.format(a=base_color, b=next_color), True, pygame.color.Color('black'))

    step += 1
    if step < number_of_steps:
        # (y-x)/number_of_steps calculates the amount of change per step required to 
        # fade one channel of the old color to the new color
        # We multiply it with the current step counter
        current_color = [x + (((y-x)/number_of_steps)*step) for x, y in zip(pygame.color.Color(base_color), pygame.color.Color(next_color))]
    else:
        step = 1
        base_color = next_color
        next_color = next(colors)

    screen.fill(pygame.color.Color('white'))
    pygame.draw.circle(screen, current_color, screen.get_rect().center, 100)
    screen.blit(text, (230, 100))
    pygame.display.update()
    clock.tick(FPS)