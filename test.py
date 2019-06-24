import pygame, sys
import numpy as np
from logic import Game, GameOverError

pygame.init()

size= (5, 5)

game = Game(size= size, difficulty= 1, seed= 0,
            fixed_goal= True, visualize= True, 
            max_screen_size= 500, turn_penalty= 0)

move_dict = {
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

            try:
                action = move_dict[event.key]
                grid, reward, game_over = game.move(action)
                #print(grid)
                print(reward, game_over)
            except GameOverError:
                print("Game Over.")

            except KeyError:
                print("Wrong Input.")