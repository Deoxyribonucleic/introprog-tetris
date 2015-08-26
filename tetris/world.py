#!/usr/bin/python
# -*- coding: utf-8 -*-

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.world = [[None for x in range(width)] for x in range(height)]

    def add_block(self, block):
        for (ypos, yline) in enumerate(block.shape):
            for (xpos, xline) in enumerate(yline):
                if block.shape[ypos][xpos] != 0:
                    self.world[block.ypos+ypos][block.xpos+xpos] = block.representation

    def collides(self, block):
        for (ypos, yline) in enumerate(block.shape):
            for (xpos, xline) in enumerate(yline):
                if block.shape[ypos][xpos] != 0 and (block.ypos + ypos < 0 or block.ypos + ypos >= self.height or block.xpos + xpos < 0 or block.xpos + xpos >= self.width or self.world[block.ypos+ypos][block.xpos+xpos] != None):
                    return True
        return False
        
