import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from device_summarizer import aggregate_by_device, filter_hot_devices


class AggregationTests(unittest.TestCase):
    def test_aggregate_and_filter(self):
        rows = [
            {"device_id": "A", "status": "ACTIVE", "temperature": "50"},
            {"device_id": "A", "status": "error", "temperature": "70"},
            {"device_id": "A", "status": "ACTIVE", "temperature": "bad"},
            {"device_id": "B", "status": "ACTIVE", "temperature": "90"},
        ]
        summary = aggregate_by_device(rows)
        self.assertEqual(summary[0]["total_records"], 3)
        self.assertEqual(summary[0]["average_temperature"], 60.0)
        self.assertEqual(summary[0]["error_count"], 1)
        self.assertEqual([d["device_id"] for d in filter_hot_devices(summary)], ["A"])


if __name__ == "__main__":
    unittest.main()
