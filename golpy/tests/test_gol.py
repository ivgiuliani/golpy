import unittest
import itertools

from golpy import patterns
from golpy.gol import GameOfLife, life_alternative, translate_cfg


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
        g = GameOfLife(patterns.BLOCK)
        for i in range(100):
            self.assertEqual(patterns.BLOCK, g.advance(i))

    def test_beehive(self):
        # a beehive is a still life
        g = GameOfLife(patterns.BEEHIVE)
        for i in range(100):
            self.assertEqual(patterns.BEEHIVE, g.advance(i))

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
        """Check that the gol is an infinitely iterable object
        (however cut to 100 iterations because we don't have infinite time)
        """
        g = GameOfLife(patterns.BLOCK)
        iterations = 0
        for state in itertools.islice(g, 100):
            iterations += 1
            self.assertEqual(patterns.BLOCK, state)
            self.assertEqual(iterations, g.iteration)
        self.assertEqual(100, iterations)

    def test_current(self):
        g = GameOfLife(patterns.BLINKER_P1)
        ptns = [patterns.BLINKER_P1, patterns.BLINKER_P2]
        for i in range(100):
            self.assertEqual(ptns[i % len(ptns)], g.current())
            g.advance()

    def test_alternative_tick(self):
        """Test that we can switch to alternative tick functions"""
        g = GameOfLife(patterns.BEEHIVE, life_function=life_alternative)
        for i in range(10):
            self.assertEqual(patterns.BEEHIVE, g.advance(i))

    def test_translate_cfg(self):
        self.assertEqual(set(), translate_cfg(set(), 0, 0))
        self.assertEqual({(0, 0)}, translate_cfg({(0, 0)}, 0, 0))
        self.assertEqual({(10, 20)}, translate_cfg({(0, 0)}, 10, 20))
        self.assertEqual({(10, 20), (20, 40)},
                         translate_cfg({(0, 0), (10, 20)}, 10, 20))
        self.assertEqual({(-10, -20)}, translate_cfg({(0, 0)}, -10, -20))

if __name__ == "__main__":
    unittest.main()
