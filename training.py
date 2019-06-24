import numpy as np
from logic import Game, GameOverError
import pygame, sys
import time
import random

print("Initailizing")
pygame.init()
print("Initialized")

max_screen_size = 500
size = (5, 5)
lr = 0.01
discount = 0.9
difficulty = 1

seed = 51

q_table_size = (*size, 4)


def print_q_table(q_table):
    for row in q_table:
        for col in row:
            print(np.round(col, decimals= 1), end=", ")
        print()

q_table = np.zeros(q_table_size)

for i in range(1, 501):
    print(i)
    use_table = False
    if i % 10 == 0:
        print(i)
        use_table = True
    
    visualize = use_table

    game = Game(size=size, difficulty= difficulty, seed= seed,
                fixed_goal= True, visualize= visualize, 
                max_screen_size= max_screen_size, turn_penalty= 0)
    game_over = False
    while not game_over:
        actions = ["left", "right", "up", "down"]

        player_pos = game.board.player_pos
        if use_table:
            ind = np.argmax(q_table[player_pos])
            action = actions[ind]
        else:
            ind, action = random.choice([*enumerate(actions)])

        grid, reward, game_over = game.move(action)
        new_player_pos = game.board.player_pos

        prev_value = q_table[player_pos][ind]

        next_max_val = max(q_table[new_player_pos])
        q_table[player_pos][ind] = q_table[player_pos][ind] + lr * (reward \
            + discount * next_max_val - q_table[player_pos][ind])

        new_value = q_table[player_pos][ind]


        if use_table:
            game.board.draw.draw_squares()
            game.board.draw.draw_table(q_table)
            #print(reward, prev_value - new_value)
            time.sleep(0.1)

        
        if (q_table > 100).any():
            print("Shit happenend: {}".format(i))
            print_q_table(np.round(q_table))
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()