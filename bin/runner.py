import sys

from golpy import gol
from golpy import animator
from golpy import patterns
from golpy import loader


def main(args):
    if len(args) > 1:
        seed = loader.rle_loader(file(args[1]))
    else:
        seed = patterns.KAREL_P15  # or any other pattern

    game = gol.GameOfLife(seed)
    animator.curses_animator(game, delay=10)

    return False


if __name__ == "__main__":
    sys.exit(main(sys.argv))
