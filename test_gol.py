import unittest
import itertools

from golpy import patterns
from golpy.gol import GameOfLife


class TestGameOfLife(unittest.TestCase):
    def test_invalid_steps(self):
        with self.assertRaises(ValueError):
            GameOfLife(set()).advance(-1)

    def test_empty(self):
        self.assertEqual(set(), GameOfLife(set()).advance(1))
        self.assertEqual(set(), GameOfLife(set()).advance(10))
        self.assertEqual(set(), GameOfLife(set()).advance(100))
        self.assertEqual(set(), GameOfLife(set()).advance(1000))

    def test_simplest(self):
        self.assertEqual(set(), GameOfLife({(1, 1)}).advance(1))

    def test_two_cells(self):
        self.assertEqual(set(), GameOfLife({(1, 1), (1, 2)}).advance(1))

    def test_blinker(self):
        self.assertEqual(patterns.BLINKER_P2,
                         GameOfLife(patterns.BLINKER_P1).advance(1))

    def test_toad(self):
        self.assertEqual(patterns.TOAD_P2,
                         GameOfLife(patterns.TOAD_P1).advance(1))

    def test_block(self):
        # a block is a still life
        for i in range(100):
            self.assertEqual(patterns.BLOCK, GameOfLife(patterns.BLOCK).advance(i))

    def test_beehive(self):
        # a beehive is a still life
        for i in range(100):
            self.assertEqual(patterns.BEEHIVE, GameOfLife(patterns.BEEHIVE).advance(i))

    def test_iteration_count(self):
        g = GameOfLife(set())

        g.advance(0)
        self.assertEqual(0, g.iteration)

        g.advance(1)
        self.assertEqual(1, g.iteration)

        g.advance(10)
        self.assertEqual(11, g.iteration)

        g.advance(100)
        self.assertEqual(111, g.iteration)

    def test_iterable(self):
        g = GameOfLife(patterns.BLOCK)
        # check that the gol is an infinitely iterable object
        # (however cut to 100 iterations because we don't have infinite time)
        iterations = 0
        for state in itertools.islice(g, 100):
            iterations += 1
            self.assertEqual(patterns.BLOCK, state)
            self.assertEqual(iterations, g.iteration)
        self.assertEqual(100, iterations)


if __name__ == "__main__":
    unittest.main()
