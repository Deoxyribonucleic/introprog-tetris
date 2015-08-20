import curses

class WorldRenderer:
    def __init__(self, window):
        self.window = window

    def draw(self, world):
        self._draw_block(0, 0, 0)

    def _draw_block(self, x, y, block_type):
        for offset_x in range(0, 3):
            for offset_y in range(0, 2):
                self.window.addch(y + offset_y + 1, x + offset_x + 1, 'X') # +1 on both to accomodate for border

