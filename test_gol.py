import unittest

from gol import GameOfLife


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
    unittest.main()
