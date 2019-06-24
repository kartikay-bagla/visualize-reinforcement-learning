import sys, pygame
import numpy as np
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

color_dict = {
    1: BLUE,
    2: RED,
    5: GREEN
}

class Draw(object):
    def __init__(self, grid_size, max_size= 800):
        self.grid_size = grid_size
        self.set_screen(max_size)
        self.draw_squares()
        self.font = pygame.font.Font(None, self.font_size)
        pygame.display.flip()

    def set_screen(self, max_size):
        if self.grid_size[0] > self.grid_size[1]:
            self.height = max_size
            self.width = int(self.height * self.grid_size[1] / self.grid_size[0])
            self.font_size = (self.width // self.grid_size[1]) // 4
            
        else:
            self.width = max_size
            self.height = int(self.width * self.grid_size[0] / self.grid_size[1])
            self.font_size = (self.height // self.grid_size[0]) // 4
            

        self.size = self.width, self.height

        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(BLACK)


        widths = np.linspace(0, self.width, num= self.grid_size[1] + 1, dtype= int)
        for pos in widths:
            start_pos, end_pos = (pos, 0), (pos, self.height)
            line = pygame.draw.line(self.screen, WHITE, start_pos, end_pos, 3)

    def draw_squares(self):
        h_squares, w_squares = self.grid_size

        h_dist = int(self.height / h_squares)
        w_dist = int(self.width / w_squares)

        self.grid_rects = np.zeros((h_squares, w_squares, 4))

        for i in range(h_squares):
            for j in range(w_squares):
                rect = pygame.draw.rect(self.screen, WHITE, [j * w_dist, i * h_dist, w_dist, h_dist], 1)
                self.grid_rects[i, j] = rect

    def fill_square(self, index, color):
        curr_rect = self.grid_rects[index]
        pygame.draw.rect(self.screen, color, curr_rect, 0)
        pygame.display.flip()

    def update(self, gameGrid, q_table= None):
        self.screen.fill(BLACK)
        
        for i in range(len(gameGrid)):
            for j in range(len(gameGrid[i])):
                try:
                    color = color_dict[gameGrid[i, j]]
                    self.fill_square((i, j), color)
                except KeyError:
                    pass

        self.draw_squares()

        if q_table is not None:
            self.draw_table(q_table)

        pygame.display.flip()

    def draw_table(self, q_table):
        q_table = np.round(q_table, decimals= 2)
        for i in range(len(q_table)):
            for j in range(len(q_table[i])):
                r = self.grid_rects[i][j]
                rect = pygame.rect.Rect(*r)
                # It works
                positions = [
                    np.array(rect.midleft) \
                      + (np.array(rect.center) \
                          - np.array(rect.midleft)) // 2,
                    np.array(rect.center) \
                      + (np.array(rect.midright) \
                          - np.array(rect.center)) // 2,
                    np.array(rect.midtop) \
                      + (np.array(rect.center) \
                          - np.array(rect.midtop)) // 2,
                    np.array(rect.center) \
                      + (np.array(rect.midbottom) \
                          - np.array(rect.center)) // 2
                ]

                for k in range(4):
                    pos = positions[k]

                    text = self.font.render(str(q_table[i, j, k]), 
                                        True, WHITE)

                    self.screen.blit(
                        text, 
                        (pos[0] - text.get_width() // 2,
                        pos[1] - text.get_height() // 2)
                    )

        pygame.display.flip()
                
if __name__ == "__main__":
    pygame.init()

    draw = Draw((5, 10), 500)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()