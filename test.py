import unittest

from main import soft_number_list


class TestUtils(unittest.TestCase):
    def test_soft_number_list(self):
        self.assertListEqual(soft_number_list([1, 1, 1, 1, 2, 3], 3), [1, 1, (4 / 3), 2])
        self.assertListEqual(soft_number_list([7, 8, 42, -9, 0, -3], 1), [7, 8, 42, -9, 0, -3])
        self.assertListEqual(soft_number_list([7, 8, 42, -9, 0, -3], 3), [57 / 3, 41 / 3, 11, -4])


if __name__ == "__main__":
    unittest.main()
