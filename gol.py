import time

from collections import defaultdict, Counter

__all__ = ["GameOfLife", "generate_neighbours", "translate_cfg"]


class GameOfLife(object):
    """
    Conway's Game of Life
    """

    def __init__(self, seed, tick_function=None):
        seed = frozenset(seed)
        self.__config = seed
        self.__iteration = 0
        self.__tick_function = tick_function or self.__tick

    def __iter__(self):
        return self

    def next(self):
        # yields an infinite generator
        return self.advance(1)

    def advance(self, n=1):
        if n < 0:
            raise ValueError("the number of steps can't be negative")

        for i in range(n):
            self.__config = self.__tick_function(self.__config)
            self.__iteration += 1
        return self.__config

    @property
    def iteration(self):
        """
        The current iteration count.
        """
        return self.__iteration

    def current(self):
        """
        Returns an immutable copy of the current state.
        @return: a copy of the current state
        @rtype: set
        """
        return frozenset(self.__config)

    @staticmethod
    def __tick(config):
        """
        Applies Game of Life's rules to obtain a new state from the given
        input state.

        @param config: input configuration as a set of pairs (x, y)
        @type config: frozenset
        @return: output configuration of the next step as a set of pairs (x, y)
        @rtype: frozenset
        """
        dd = defaultdict(int)
        for x, y in config:
            for nx, ny in generate_neighbours(x, y):
                dd[(nx, ny)] += 1

        survivors = {key for key, val in dd.items() if val in (2, 3)} & config
        back_from_dead = {key for key, val in dd.items() if val == 3} - config

        return frozenset(survivors | back_from_dead)


def __tick_alternative(config):
    """
    Applies Game of Life's rules to obtain a new state from the given
    input state.

    This implementation differs from the original approach in that it uses
    a counter rather than a defaultdict to group the same items together.
    However it's slightly slower than the original approuch, but the cause
    it's certainly worth investigating.

    @param config: input configuration as a set of pairs (x, y)
    @type config: frozenset
    @return: output configuration of the next step as a set of pairs (x, y)
    @rtype: frozenset
    """

    dd = Counter([
        item for x, y in config for item in generate_neighbours(x, y)
    ])

    survivors = {key for key, val in dd.items() if val in (2, 3)} & config
    back_from_dead = {key for key, val in dd.items() if val == 3} - config

    return frozenset(survivors | back_from_dead)


def generate_neighbours(x, y):
    return {
        # in clockwise sense
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        (x - 1,     y),             (x + 1,     y),
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
    }


def animate(cfgs, grid_top_left, grid_bottom_right, delay=50):
    """
    Animate the given configurations on the screen.
    """
    import curses
    wnd = curses.initscr()

    def print_cfg(cfg):
        start_x, start_y = grid_top_left
        stop_x, stop_y = grid_bottom_right
        for y in range(start_y, stop_y + 1):
            for x in range(start_x, stop_x + 1):
                val = (x, y) in cfg and "#" or " "
                wnd.addch(y, x, val)
        wnd.refresh()

    try:
        for config in cfgs:
            print_cfg(config)
            time.sleep(delay / 100.0)
    except KeyboardInterrupt:
        curses.endwin()


def translate_cfg(cfg, x, y):
    """
    Translates a given configuration expressed as a set of coordinates of the
    specified amount in the x and y axis.
    @returns: the translated configuration
    @rtype: set
    """
    return {(c_x + x, c_y + y) for c_x, c_y in cfg}


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


if __name__ == "__main__":
    start = GameOfLife(translate_cfg(PATTERN_KAREL_P15, 40, 20))
    animate(start, (0, 0), (80, 50), delay=10)
