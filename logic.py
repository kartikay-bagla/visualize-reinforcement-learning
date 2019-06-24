from game_class import Board

class GameOverError(Exception):
    pass

class Game:
    def __init__(self, size= (5, 5), difficulty= 1, seed= None, fixed_goal= False, visualize= True, max_screen_size= 800, turn_penalty= 1):
        
        self.board = Board(size, difficulty, seed, 
                           fixed_goal, visualize, max_screen_size)
        self.reward = 0
        self.turn_penalty = turn_penalty
        self.obstacle_penalty = 2
        self.win_bonus= 10
        self.game_over = False

    def move(self, action):

        if self.game_over:
            raise GameOverError

        turn_reward = 0

        curr_grid = self.board.grid
        loc = self.board.player_pos
        if action == "up":
            new_loc = (loc[0] - 1, loc[1])
        elif action == "down":
            new_loc = (loc[0] + 1, loc[1])
        elif action == "left":
            new_loc = (loc[0], loc[1] - 1)
        elif action == "right":
            new_loc = (loc[0], loc[1] + 1)
        else:
            raise ValueError("action is not valid")

        can_move, output = self.board.check_location(new_loc)
        if can_move:
            self.board.change_player_pos(new_loc)

        if output in ["obstacle", "boundary"]:
            turn_reward -= self.obstacle_penalty
        elif output == "goal":
            turn_reward += self.win_bonus
            self.game_over = True

        turn_reward -= self.turn_penalty

        self.reward += turn_reward

        return self.board.grid, turn_reward, self.game_over

            
