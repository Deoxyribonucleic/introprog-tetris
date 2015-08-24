import tetris.gui
import tetris.block
import tetris.world

import time

class Game:
    def __init__(self):
        self.tick_interval = 1
        self.points = 0

        self.world_width = 13
        self.world_height = 15
        
        self.world = tetris.world.World(self.world_width, self.world_height)

        self.world.add_block(tetris.block.Block(tetris.block.blocks[0]))
        self.world.add_block(tetris.block.Block(tetris.block.blocks[1], 3, 5))


    def __enter__(self):
        self.gui = tetris.gui.GUI()
        return self

    def run(self):
        self.start = time.time()
        self.last_tick = self.start

        # render once at start
        self.gui.draw_status(None, None)
        self.gui.draw_game(self.world)

        while True:
            action = self.gui.get_input((self.last_tick + self.tick_interval) - time.time())
            if action != None:
                self.gui.status_window.addch(action)
                self.gui.draw_game(self.world)

            if time.time() > (self.last_tick + self.tick_interval):
                self.tick()
            
    def tick(self):
        self.gui.status_window.addch('T')
        self.last_tick = time.time()

        self.points += 1 #flyttas till där man ska få poäng

        if self.tick_interval <= 0.2:
            self.tick_interval = 0.95 ** self.points

        self.gui.draw_game(self.world)
        self.gui.draw_status(None, None)

    def __exit__(self, exc_type, exc_value, traceback):
        self.gui.destroy()

