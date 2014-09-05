from collections import defaultdict, Counter

__all__ = ["GameOfLife", "generate_neighbours", "translate_cfg"]


class GameOfLife(object):
    """
    Conway's Game of Life
    """

    def __init__(self, seed, life_function=None):
        """
        Initializes the state of a Game of Life with a given seed.
        @param seed: the start configuration of this particular instance of
                     the Game of Life. This must be a list of pairs (x,y)
                     specifying the coordinates of the alive cells in the board
                     (the coordinate (0,0) is assumed to be the top-left
                     corner).
        """
        seed = frozenset(seed)
        self.__state = seed
        self.__iteration = 0
        self.__life_function = life_function or self.__life

    def __iter__(self):
        return self

    def next(self):
        # required for python2 backwards compatibility
        return self.__next__()

    def __next__(self):
        # yields an infinite generator
        return self.advance(1)

    def advance(self, n=1):
        """
        Advances the game of life of the specified amount of steps.
        @param n: number of steps to advance
        @type n: int
        @return: the game of life status after advancing for the specified
                 step count
        """
        if n < 0:
            raise ValueError("the number of steps can't be negative")

        for i in range(n):
            self.__state = self.__life_function(self.__state)
            self.__iteration += 1
        return self.__state

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
        return frozenset(self.__state)

    @staticmethod
    def __life(config):
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

        survivors = {key for key, val in dd.items() if val in (2, 3)}
        back_from_dead = {key for key, val in dd.items() if val == 3}

        return frozenset((survivors & config) | (back_from_dead - config))


def life_alternative(config):
    """
    Applies Game of Life's rules to obtain a new state from the given
    input state.

    This implementation differs from the original approach in that it uses
    a counter rather than a defaultdict to group the same items together.
    However it's slightly slower than the original approach, but the cause
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
    return (
        # in clockwise sense
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        (x - 1,     y),             (x + 1,     y),
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
    )


def translate_cfg(cfg, x, y):
    """
    Translates a given configuration expressed as a set of coordinates by the
    specified amount in the x and y axis.

    @returns: the translated configuration
    @rtype: set
    """
    return {(c_x + x, c_y + y) for c_x, c_y in cfg}
