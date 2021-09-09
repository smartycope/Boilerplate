from Game import Game

import argparse
description = ''
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-v' , '--verbose' , action='store_true')
args = parser.parse_args()

if __name__ == "__main__":
    game = Game(args=args, size=[720, 720])
    game.run()
    game.currentScene.exit()
