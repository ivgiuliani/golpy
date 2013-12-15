import sys

from golpy import gol
from golpy import animator
from golpy import patterns


def main(args):
    start = gol.GameOfLife(patterns.KAREL_P15)
    animator.curses_animator(start, delay=10)
    return False


if __name__ == "__main__":
    sys.exit(main(sys.argv))

