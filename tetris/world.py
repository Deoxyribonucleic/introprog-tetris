#!/usr/bin/python
# -*- coding: utf-8 -*-

class World:
    def __init__(self, width, height):
        self.world = [[None for x in range(width)] for x in range(height)]

    def add_block(self, block):
        for (ypos, yline) in enumerate(block.shape):
            for (xpos, xline) in enumerate(yline):
                if block.shape[ypos][xpos] != 0:
                    self.world[block.ypos+ypos][block.xpos+xpos] = block.representation

    def collides(self, block):
        for col in range(len(block.shape[0])):

