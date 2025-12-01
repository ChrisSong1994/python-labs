import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from tp_utils import add


class TestAdd(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add(1, 2), 3)

    def test_add_floats(self):
        self.assertEqual(add(3.5, 4.5), 8.0)

    def test_add_mixed_int_float(self):
        self.assertEqual(add(10, 20.5), 30.5)

    def test_batch_add_list(self):
        self.assertEqual(add([1, 2, 3, 4]), 10)

    def test_batch_add_tuple(self):
        self.assertEqual(add((5, 6, 7)), 18)

    def test_non_strict_string_number(self):
        self.assertEqual(add("1", 2, strict_type=False), 3)

    def test_non_strict_batch_strings(self):
        self.assertEqual(add(["1", "2.5"], strict_type=False), 3.5)

    def test_strict_type_error_on_string(self):
        with self.assertRaises(TypeError):
            add("1", 2)

    def test_batch_requires_sequence(self):
        with self.assertRaises(ValueError):
            add(1)

    def test_single_add_disallows_sequence_a(self):
        with self.assertRaises(TypeError):
            add([1, 2], 3)

    def test_non_strict_invalid_string_raises(self):
        with self.assertRaises(TypeError):
            add(["x", 2], strict_type=False)


if __name__ == "__main__":
    unittest.main()
