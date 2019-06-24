import numpy as np 
import pygame
from draw_class import Draw
import sys

pygame.init()

size = (5, 5)
q_table_size = (*size, 4)

q_table = np.zeros(q_table_size)

draw = Draw(size)
draw.draw_table(q_table)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()