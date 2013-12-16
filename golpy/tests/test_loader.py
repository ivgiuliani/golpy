import unittest

from golpy.loader import rle_loader


class TestRLELoader(unittest.TestCase):
    @staticmethod
    def gen(items=None):
        return ["x=0, y=0"] + items or []

    def test_empty(self):
        self.assertEqual(set(), rle_loader([]))

    def test_oneitem(self):
        self.assertEqual({(3, 0)}, rle_loader(self.gen(["3bo$"])))

    def test_missing_endline_marker(self):
        self.assertEqual({(3, 0)}, rle_loader(self.gen(["3bo"])))

    def test_two_lines(self):
        self.assertEqual({(3, 0), (4, 1)}, rle_loader(self.gen(["3bo$4bo!"])))

    def test_no_numbers(self):
        self.assertEqual({
            (1, 0), (3, 0), (5, 0)
        }, rle_loader(self.gen(["bobobo"])))

    def test_simple_configuration(self):
        self.assertEqual({
            (6, 0), (35, 0), (37, 0), (45, 0)
        }, rle_loader(self.gen(["6bo28bobo7bo18b$"])))

    def test_large_config_but_one_alive(self):
        self.assertEqual({(999999, 0)}, rle_loader(self.gen(["999999bo$"])))

    def test_comments_are_ignored(self):
        self.assertEqual({(3, 1)}, rle_loader([
            "# comment line 1", "# comment line 2", "x=0, y=0", "bbb$3bo$"
        ]))

if __name__ == "__main__":
    unittest.main()
