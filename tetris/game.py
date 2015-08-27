#!/usr/bin/python
# -*- coding: utf-8 -*-

import tetris.gui
import tetris.block
import tetris.world

import os
import time
import random
import copy

class Game:
    def __init__(self, height):
        self.quit = False
        self.tick_interval = 1

        self.world_width = 10
        self.world_height = height 

        self.highscore = 0
        self.read_highscore()

        random.seed(time.time())
        self.reset_game()

    def __enter__(self):
        self.gui = tetris.gui.GUI(self.world_width, self.world_height)
        return self

    def read_highscore(self):
        try:
            with open(os.getenv("HOME") + '/.textris', 'r') as highscore_file:
                self.highscore = int(highscore_file.read())
        except IOError:
            self.write_highscore()

    def write_highscore(self):
        with open(os.getenv("HOME") + '/.textris', 'w') as highscore_file:
            return highscore_file.write(str(self.highscore))

    def reset_game(self):
        self.points = 0
        self.level = 1
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

        block = tetris.block.Block(self.block_bag.pop(), self.world_width / 2, 0)
        # rotate randomly
        for x in range(0, random.randint(0, 3)):
            block.rotate()
        return block

    def run(self):
        self.start = time.time()
        self.last_tick = self.start

        # render once at start
        self.gui.draw_status(self.next_block, self.points, self.level, self.highscore)
        self.gui.draw_game(self.world, self.current_block)

        while not self.quit:
            if self.current_block == None:
                self.current_block = self.next_block
                self.next_block = self.create_random_block()
                self.gui.draw_game(self.world, self.current_block)
                self.gui.draw_status(self.next_block, self.points, self.level, self.highscore)

            self.handle_input()

            if time.time() > (self.last_tick + self.tick_interval):
                self.tick()

            self.remove_full_lines()
            self.check_game_over()


    def handle_input(self):
        action = self.gui.get_input((self.last_tick + self.tick_interval) - time.time())

        if action != None:
            if action == Action.quit:
                self.quit = True

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

    def check_game_over(self):
        if self.world.game_over():
            play_again = self.gui.prompt_play_again(self.points, self.highscore)
            if self.points > self.highscore:
                self.highscore = self.points

            if play_again:
                self.reset_game()
            else:
                self.quit = True

    def remove_full_lines(self):
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
        if self.points > self.highscore:
            self.highscore = self.points
            self.write_highscore()
        self.gui.destroy()

class Action:
    rotate = 1
    down = 2
    move_left = 3
    move_right = 4
    quit = 5

