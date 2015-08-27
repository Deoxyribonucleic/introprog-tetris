#!/usr/bin/python
# -*- coding: utf-8 -*-

import tetris.game
import argparse

parser = argparse.ArgumentParser(description='Play some Textris')
parser.add_argument('--height',
                    dest='height',
                    default=22,
                    type=int,
                    help='Specify the height of the window between 12 and 22. Defaults to 22.')
args = parser.parse_args()

if args.height < 12 or args.height > 22:
    print('Height must be between 12 and 22')
    exit()

with tetris.game.Game(args.height) as game:
    game.run()
