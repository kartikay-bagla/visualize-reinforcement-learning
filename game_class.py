import numpy as np
from draw_class import Draw



class Board(object):
    mapping = {
        "player": 1,
        "obstacle": 2,
        "goal": 5,
        "empty": 0
    }
    reverse_map = dict(reversed(item) for item in mapping.items())
    
    def __init__(self, size=(5, 5), difficulty= 1, seed= None, fixed_goal= False, visualize= True, max_screen_size= 800):
        self.size = size
        self.difficulty = difficulty

        if seed is not None:
            np.random.seed(seed)
        self.fixed_goal = fixed_goal
        self.grid = np.zeros(shape= self.size, dtype= int)

        self.initialize_grid()
        
        self.visualize = visualize
        self.max_screen_size = max_screen_size

        if self.visualize:
            print("Initalizing graphics")
            self.initialize_graphics()

    def initialize_grid(self):
        rInt = np.random.randint
        self.player_pos = (self.size[0] - 1, 0)
        
        if self.fixed_goal:
            self.goal = (0, self.size[1] - 1)
        else:
            while True:
                self.goal = (rInt(0, self.size[0]), rInt(0, self.size[1]))
                if self.goal != self.player_pos:
                    break

        self.num_obs = self.difficulty * 3
        self.obs = []
        while len(self.obs) < self.num_obs:
            new_obs = (rInt(0, self.size[0]), rInt(0, self.size[1]))
            if new_obs != self.goal and new_obs != self.player_pos and new_obs not in self.obs:
                self.obs.append(new_obs)

        self.grid[self.player_pos] = Board.mapping["player"]
        self.grid[self.goal] = Board.mapping["goal"]
        for obstacle in self.obs:
            self.grid[obstacle] = Board.mapping["obstacle"]

    def initialize_graphics(self):
        self.draw = Draw(self.size, self.max_screen_size)
        self.draw.update(self.grid)

    def change_player_pos(self, new_loc):
        self.grid[self.player_pos] = 0
        self.player_pos = new_loc
        self.grid[self.player_pos] = Board.mapping["player"]
        if self.visualize:
            self.draw.update(self.grid)

    def check_location(self, new_loc):
        try:
            if new_loc[0] < 0 or new_loc[1] < 0:
                raise IndexError
            
            value = self.grid[new_loc]
            if Board.reverse_map[value] == "obstacle":
                return False, Board.reverse_map[value]
            elif Board.reverse_map[value] == "goal":
                return True, "goal"
            else:
                return True, "empty"
            
        except IndexError:
            return False, "boundary"

    def __str__(self):
        return str(self.grid)

    def __repr__(self):
        return "Board{}".format(self.size) + "\n" + self.__str__()

if __name__ == "__main__":
    board = Board(size= (10, 10), difficulty= 5, seed= 0, fixed_goal= True)
    print(board)