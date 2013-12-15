import unittest

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
        self.assertEqual({(3, 2), (3, 3), (3, 4)},
                         GameOfLife({(2, 3), (3, 3), (4, 3)}).advance(1))

    def test_toad(self):
        start = {(3, 3), (4, 3), (5, 3), (2, 4), (3, 4), (4, 4)}
        stop = {(4, 2), (2, 3), (5, 3), (2, 4), (5, 4), (3, 5)}
        self.assertEqual(start, GameOfLife(stop).advance(1))

    def test_block(self):
        # a block is a still life
        block = {(2, 2), (3, 2), (2, 3), (3, 3)}
        for i in range(100):
            self.assertEqual(block, GameOfLife(block).advance(i))

    def test_beehive(self):
        # a beehive is a still life
        block = {(3, 2), (4, 2), (2, 3), (5, 3), (3, 4), (4, 4)}
        for i in range(100):
            self.assertEqual(block, GameOfLife(block).advance(i))

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


if __name__ == "__main__":
    unittest.main()
