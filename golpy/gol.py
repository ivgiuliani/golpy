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


def translate_cfg(cfg, x, y):
    """
    Translates a given configuration expressed as a set of coordinates of the
    specified amount in the x and y axis.
    @returns: the translated configuration
    @rtype: set
    """
    return {(c_x + x, c_y + y) for c_x, c_y in cfg}
