import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sensor_cleaning import clean_sensor_data


class CleanSensorDataTests(unittest.TestCase):
    def test_mixed_input(self):
        data = [100, "200", None, -50, "abc", 600, 300.5]
        self.assertEqual(clean_sensor_data(data), [100.0, 200.0, 500.0, 300.5])

    def test_empty_list(self):
        self.assertEqual(clean_sensor_data([]), [])

    def test_all_invalid(self):
        self.assertEqual(clean_sensor_data([None, "x", -1, "", float("nan")]), [])

    def test_boundaries(self):
        self.assertEqual(clean_sensor_data([0, 500, 500.1, -0.1]), [0.0, 500.0, 500.0])

    def test_non_iterable_input(self):
        self.assertEqual(clean_sensor_data(None), [])
        self.assertEqual(clean_sensor_data(42), [])


if __name__ == "__main__":
    unittest.main()
