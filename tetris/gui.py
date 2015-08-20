import curses

class GUI:
    def __init__(self):
        self.stdscr = None
        self.input_queue = []

        self.key_binds = {
                    curses.KEY_UP: 'A',
                    curses.KEY_DOWN: 'B'
                }

        self.setup_screen()
        self.setup_windows()


    def destroy(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.curs_set(1)
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

        self.input_window = curses.newwin(0, 0, 0, 60) 
        self.input_window.keypad(1)

        self.game_window.box()
        self.status_window.box()

        self.game_window.addstr(1, 1, "hello")

        self.game_window.refresh()
        self.status_window.refresh()

    def update_game(self, world):
        self.status_window.box()
        self.status_window.refresh()
        self.game_window.box()
        self.game_window.refresh()

    def get_input(self, timeout):
        self.input_window.timeout(int(timeout * 1000))
        key = self.input_window.getch()
        if key in self.key_binds:
            return self.key_binds[key]
        else:
            return None
        

    def update_status(self, next_block, score):
        pass


