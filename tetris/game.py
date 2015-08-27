#!/usr/bin/python
# -*- coding: utf-8 -*-

import tetris.gui
import tetris.block
import tetris.world

import time
import random
import copy

class Game:
    def __init__(self):
        self.tick_interval = 1

        self.world_width = 10
        self.world_height = 22 

        random.seed(time.time())
        self.reset_game()

    def __enter__(self):
        self.gui = tetris.gui.GUI(self.world_width, self.world_height)
        return self

    def reset_game(self):
        self.points = 0
        self.level = 1
        self.highscore = 0
        self.continuous_soft_drop = 0
        self.lines_cleared = 0
        self.world = tetris.world.World(self.world_width, self.world_height)
        self.block_bag = []
        self.next_block = self.create_random_block()
        self.current_block = None

    def get_points(self, nrows):
        if nrows == 0:
            return 0
        elif nrows == 1:
            return 40 * (self.level + 1) + self.continuous_soft_drop
        elif nrows == 2:
            return 100 * (self.level + 1) + self.continuous_soft_drop
        elif nrows == 3:
            return 300 * (self.level + 1) + self.continuous_soft_drop
        else:
            return 1200 * (self.level + 1) + self.continuous_soft_drop

    def get_tick_interval(self):
        if self.level < 10:
            return 1 - self.level * .1
        else:
            return .05

    def create_random_block(self):
        if len(self.block_bag) == 0:
            self.block_bag = copy.copy(tetris.block.blocks)
            random.shuffle(self.block_bag)

        return tetris.block.Block(self.block_bag.pop(), self.world_width / 2, 0)

    def run(self):
        self.start = time.time()
        self.last_tick = self.start

        # render once at start
        self.gui.draw_status(self.next_block, self.points, self.level, self.highscore)
        self.gui.draw_game(self.world, self.current_block)

        while True:
            if self.current_block == None:
                self.current_block = self.next_block
                self.next_block = self.create_random_block()
                self.gui.draw_game(self.world, self.current_block)
                self.gui.draw_status(self.next_block, self.points, self.level, self.highscore)

            action = self.gui.get_input((self.last_tick + self.tick_interval) - time.time())

            if action != None:
                if action == Action.rotate:
                    # fix this crap
                    self.current_block.rotate()
                    # if we end up colliding, reverse operation
                    if self.world.collides(self.current_block):
                        self.current_block.rotate()
                        self.current_block.rotate() # :D
                        self.current_block.rotate()

                if action == Action.down:
                    self.tick(True)

                if action == Action.move_left:
                    self.current_block.xpos -= 1
                    if self.world.collides(self.current_block):
                        self.current_block.xpos += 1

                if action == Action.move_right:
                    self.current_block.xpos += 1
                    if self.world.collides(self.current_block):
                        self.current_block.xpos -= 1

                self.gui.draw_game(self.world, self.current_block)

            if time.time() > (self.last_tick + self.tick_interval):
                self.tick()

            rows_removed = 0
            while self.world.line_check() is not None:
                rows_removed += 1
                self.world.remove_line(self.world.line_check())

            self.points += self.get_points(rows_removed)

            if rows_removed:
                self.lines_cleared += rows_removed
                if self.lines_cleared >= 10:
                    self.lines_cleared = 0
                    self.level += 1
                    self.tick_interval = self.get_tick_interval()

            if self.world.game_over():
                play_again = self.gui.prompt_play_again(self.points, self.highscore)
                if play_again:
                    self.reset_game()
                else:
                    break


            
    def tick(self, soft_drop = False):
        if soft_drop:
            self.continuous_soft_drop += 1
        else:
            self.continuous_soft_drop = 0

        self.last_tick = time.time()

        self.current_block.ypos += 1
        if self.world.collides(self.current_block):
            self.current_block.ypos -= 1
            self.world.add_block(self.current_block)
            self.current_block = None

        self.gui.draw_game(self.world, self.current_block)
        self.gui.draw_status(self.next_block, self.points, self.level, self.highscore)

    def __exit__(self, exc_type, exc_value, traceback):
        self.gui.destroy()

class Action:
    rotate = 1
    down = 2
    move_left = 3
    move_right = 4

