#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses
import time

import renderer
import game

class GUI:
    def __init__(self, world_width, world_height):
        self.stdscr = None
        self.input_queue = []

        self.key_binds = {
                    curses.KEY_UP: game.Action.rotate,
                    curses.KEY_DOWN: game.Action.down,
                    curses.KEY_LEFT: game.Action.move_left,
                    curses.KEY_RIGHT: game.Action.move_right
                }

        self.setup_screen()
        self.setup_windows(world_width, world_height)

        
        self.world_renderer = renderer.WorldRenderer(self.game_window)
        self.next_block_renderer = renderer.NextBlockRenderer(self.next_block_window)

    def destroy(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.nl()
        curses.curs_set(1)
        curses.echo()
        curses.endwin()

    def setup_screen(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        self.init_colors()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.nonl()
        self.stdscr.keypad(1)

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def setup_windows(self, world_width, world_height):
        self.input_window = curses.newwin(self.stdscr.getmaxyx()[0] - 2, self.stdscr.getmaxyx()[1] - 2, 0, 0) # world_width * 3 + 2 + 20) 
        self.input_window.keypad(1)
        self.input_window.refresh()
        self.stdscr.refresh()

        self.game_window = curses.newwin(world_height * 2 + 2, world_width * 3 + 2, 0, 0)
        self.status_window = curses.newwin(world_height * 2 + 2, 20, 0, 0)

        self.next_block_window = self.status_window.derwin(10,14,4,3)
        self.next_block_window.box()

        self.game_window.box()
        self.status_window.box()

        self.center_windows()

        self.game_window.refresh()
        self.status_window.refresh()

    def center_windows(self):
        screen_size = self.stdscr.getmaxyx()
        game_window_size = self.game_window.getmaxyx()
        status_window_size = self.status_window.getmaxyx()

        self.game_window.mvwin(screen_size[0] / 2 - game_window_size[0] / 2,
                screen_size[1] / 2 - (game_window_size[1] + status_window_size[1]) / 2)
        self.status_window.mvwin(screen_size[0] / 2 - game_window_size[0] / 2,
                screen_size[1] / 2 - (game_window_size[1] + status_window_size[1]) / 2 + game_window_size[1])
        #self.input_window.mvwin(0,
        #        screen_size[1] / 2 - (game_window_size[1] + status_window_size[1]) / 2 + game_window_size[1] + status_window_size[1])

    def get_input(self, timeout):
        self.input_window.timeout(int(timeout * 1000))
        key = self.input_window.getch()
        if key in self.key_binds:
            return self.key_binds[key]
        else:
            return None

    def draw_game(self, world, current_block):
        self.game_window.erase()
        self.game_window.box()
        self.world_renderer.draw(world)
        if current_block:
            self.world_renderer.draw_block(current_block)
        
        self.game_window.refresh()
        
    def draw_status(self, next_block, score, level, highscore):
        self.status_window.erase()
        self.status_window.box()
        self.status_window.addstr(3,4,"Next block")
        self.next_block_window = self.status_window.derwin(10,14,4,3)
        self.next_block_window.box()

        self.status_window.addstr(19,4,"Score: " + str(score))
        self.status_window.addstr(20,4,"Level: " + str(level))
        self.status_window.addstr(22,4,"Hi-score: " + str(highscore))

        self.score_window = self.status_window.derwin(1,14,20,3) # uh?

        self.next_block_renderer.draw(next_block)
        self.next_block_window.refresh()
        self.status_window.refresh()

    def prompt_play_again(self, score, highscore):
        screen_size = self.stdscr.getmaxyx()
        prompt_window = curses.newwin(10, 24, screen_size[0]/2 - 5, screen_size[1]/2 - 12)
        prompt_window.box()

        prompt_window.addstr(2, 7, "GAME OVER!")

        score_string = "Score: " + str(score)
        prompt_window.addstr(3, 12 - len(score_string) / 2, score_string)
        prompt_window.addstr(4, 5, "New high score!")
        prompt_window.addstr(6, 7, "Play again?")

        selection = True
        prompt_window.addstr(7, 7, "")

        self.input_window.timeout(-1)

        while True:
            prompt_window.addstr(7, 7, ("[yes]" if selection else " yes ") + "  " + (" no " if selection else "[no]"))
            prompt_window.refresh()

            key = self.input_window.getch()
            if key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
                selection = not selection
            elif key == 13:
                return selection

