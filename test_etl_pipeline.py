import sqlite3
import unittest

from etl_pipeline import initialize_database, load_records, transform_and_validate


class TransformTests(unittest.TestCase):
    def test_normalizes_whitespace_and_accepts_valid_row(self):
        clean, rejected = transform_and_validate([{
            "id": 1, "userId": 2, "title": "  Hello   world ", "body": " body "
        }])
        self.assertEqual(len(clean), 1)
        self.assertEqual(clean[0]["title"], "Hello world")
        self.assertEqual(clean[0]["body"], "body")
        self.assertEqual(rejected, [])

    def test_rejects_missing_fields(self):
        clean, rejected = transform_and_validate([{"id": 1}])
        self.assertEqual(clean, [])
        self.assertEqual(len(rejected), 1)

    def test_rejects_duplicate_ids_in_same_batch(self):
        row = {"id": 1, "userId": 2, "title": "A", "body": "B"}
        clean, rejected = transform_and_validate([row, row])
        self.assertEqual(len(clean), 1)
        self.assertEqual(len(rejected), 1)


class LoadTests(unittest.TestCase):
    def test_load_is_idempotent(self):
        connection = sqlite3.connect(":memory:")
        initialize_database(connection)
        record = {
            "post_id": 1, "user_id": 2, "title": "A", "body": "B",
            "loaded_at": "2026-01-01T00:00:00+00:00"
        }
        load_records(connection, [record], [], 1)
        load_records(connection, [record], [], 1)
        count = connection.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        self.assertEqual(count, 1)
        connection.close()


if __name__ == "__main__":
    unittest.main()
