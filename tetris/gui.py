import curses

class GUI:
    def __init__(self):
        self.stdscr = None
        self.input_queue = []

        self.setup_screen()
        self.setup_windows()


    def destroy(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.curs_set(1)
        curses.nodelay(1)
        curses.echo()
        curses.endwin()

    def setup_screen(self):
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)

    def setup_windows(self):
        self.game_window = curses.newwin(30, 40, 0, 0)
        self.status_window = curses.newwin(30, 20, 0, 40)

        self.game_window.box()
        self.status_window.box()

        self.game_window.refresh()
        self.status_window.refresh()

    def update_game(self, world):
        input = self.stdscr.getch()

        if input == curses.KEY_LEFT:
            self.input_queue.append("LEFT")

    def update_status(self, next_block, score):
        pass


