#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses

import worldrenderer
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
        
        self.world_renderer = worldrenderer.WorldRenderer(self.game_window)


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

    def setup_windows(self, world_width, world_height):
        self.game_window = curses.newwin(world_height * 2 + 2, world_width * 3 + 2, 0, 0)
        self.status_window = curses.newwin(world_height * 2 + 2, 20, 0, 0)

        self.input_window = curses.newwin(0, 0, 0, 0) # world_width * 3 + 2 + 20) 
        self.input_window.keypad(1)

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
        
    def draw_status(self, next_block, score):
        self.status_window.box()
        self.status_window.refresh()

