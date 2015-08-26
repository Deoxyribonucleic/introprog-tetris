#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses
                    
class Renderer:
    def __init__(self, window):
        self.window = window
    
    def draw_block(self, block):
        for y in range(len(block.shape)):
            for x in range(len(block.shape[y])):
                if block.shape[y][x]:
                    self._draw_block_element(x + block.xpos, y + block.ypos, block.representation if block.shape[y][x] != 0 else None) 

    def _draw_block_element(self, x, y, block_type):
        for offset_x in range(0, 3):
            for offset_y in range(0, 2):
                self.window.addch(y * 2 + offset_y + 1, x * 3 + offset_x + 1, block_type) # +1 on both to accomodate for border

class WorldRenderer(Renderer):
    def draw(self, world):
        for y in range(len(world.world)):
            for x in range(len(world.world[y])):
                if world.world[y][x]:
                    self._draw_block_element(x, y, world.world[y][x]) 

class NextBlockRenderer(Renderer):
    def draw(self, next_block):
        self.next_block=next_block
        self.next_block.xpos=1
        self.next_block.ypos=2
        self.draw_block(next_block)
        
