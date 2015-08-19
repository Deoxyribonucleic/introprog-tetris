import tetris.gui
import time

class Game:
    def __init__(self):
        pass

    def __enter__(self):
        self.gui = tetris.gui.GUI()
        return self

    def run(self):
        while True:
            self.gui.update_game(None)

            while len(self.gui.input_queue > 0):
                pass


    def __exit__(self, exc_type, exc_value, traceback):
        self.gui.destroy()
