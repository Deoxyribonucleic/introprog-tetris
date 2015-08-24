import curses

class WorldRenderer:
    def __init__(self, window):
        self.window = window

    def draw(self, world):
        for x in range(len(world)):
            for y in range(len(world)):
                self._draw_block(x, y, world[x][y]) 

    def _draw_block(self, x, y, block_type):
        for offset_x in range(0, 3):
            for offset_y in range(0, 2):
                self.window.addch(y * 2 + offset_y + 1, x * 3 + offset_x + 1, block_type) # +1 on both to accomodate for border

