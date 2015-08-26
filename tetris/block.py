#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy


class Block:
    def __init__(self, block_type, xpos=0, ypos=0):
        self.shape = copy.deepcopy(block_type["shape"])
        self.representation = block_type["representation"]
        self.xpos = xpos
        self.ypos = ypos

    def rotate(self):
    #     for (n,row) in enumerate(self.shape):
    #         for (m,elem) in enumerate(row):
    #             if elem == 2:
    #                 self.xpos = self.xpos - n
    #                 self.ypos = self.ypos - m
        self.shape = [[e[len(self.shape[0])-1-i] for e in self.shape] for i in range(len(self.shape[0]))]


blocks = [
    {
        "shape": 
        [
            [0,1,0],
            [0,1,0],
            [0,1,0],
            [0,1,0]
        ],
        "representation": 'I'
    },
    {
        "shape":
        [
            [0,1,0],
            [0,1,1],
            [0,1,0]
        ],
        "representation": 'T'
    },
    {
        "shape":
        [
            [1,1],
            [1,1]
        ],
        "representation": 'O'
    },
    {
        "shape":
        [
            [0,1,0],
            [0,1,0],
            [0,1,1]
        ],
        "representation": 'L'
    },
    {
        "shape":
        [
            [0,1,0],
            [0,1,0],
            [1,1,0]
        ],
        "representation": 'J'
    },
    {
        "shape":
        [
            [1,0],
            [1,1],
            [0,1]
        ],
        "representation": 'S'
    }
]
