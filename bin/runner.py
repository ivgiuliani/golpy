import sys

from golpy import gol
from golpy import animator


PATTERN_TOAD = {(3, 3), (4, 3), (5, 3), (2, 4), (3, 4), (4, 4)}
PATTERN_PI_HEPTONIMO = {(2, 4), (3, 4), (3, 3), (4, 2), (5, 3), (5, 4), (6, 4)}
PATTERN_LIGHTBULB = {
    (3, 2), (4, 2), (6, 2), (3, 3), (5, 3), (6, 3),
    (4, 5), (5, 5), (6, 5),
    (3, 6), (7, 6),
    (3, 7), (7, 7),
    (4, 8), (6, 8),
    (2, 9), (4, 9), (6, 9), (8, 9),
    (2, 10), (3, 10), (7, 10), (8, 10)
}
PATTERN_KAREL_P15 = {
    (4, 2), (9, 2),
    (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
    (4, 4), (9, 4),
    (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
    (3, 9), (10, 9),
    (2, 10), (11, 10),
    (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11),
    (3, 12), (10, 12),
}


def main(args):
    start = gol.GameOfLife(PATTERN_KAREL_P15)
    animator.curses_animator(start, delay=10)
    return False


if __name__ == "__main__":
    sys.exit(main(sys.argv))

