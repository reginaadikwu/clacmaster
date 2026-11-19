import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database

from database import initialize_database
from history import (
    add_calculation,
    get_calculation_history,
    get_calculation_by_id,
    delete_calculation,
    clear_calculation_history
)
from saved_calculations import (
    save_calculation,
    get_saved_calculations,
    get_saved_calculation,
    delete_saved_calculation
)


class TestPhase5Database(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        data_path = Path(self.temp_dir.name)

        self.data_patch = patch.object(
            database, "DATA_DIR", data_path
        )
        self.database_patch = patch.object(
            database, "DATABASE_PATH",
            data_path / "test.db"
        )

        self.data_patch.start()
        self.database_patch.start()

        initialize_database()

    def tearDown(self):
        self.database_patch.stop()
        self.data_patch.stop()
        self.temp_dir.cleanup()

    # Calculation history tests

    def test_add_calculation(self):
        record_id = add_calculation("add", "10 + 5", 15)

        self.assertIsInstance(record_id, int)

    def test_get_calculation_history(self):
        add_calculation("add", "10 + 5", 15)

        history = get_calculation_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["expression"], "10 + 5")


    def test_get_calculation_by_id(self):
        record_id = add_calculation("add", "10 + 5", 15)

        calculation = get_calculation_by_id(record_id)

        self.assertEqual(calculation["expression"], "10 + 5")
        self.assertEqual(calculation["result"], "15")

    def test_get_nonexistent_calculation_by_id(self):
        calculation = get_calculation_by_id(9999)

        self.assertIsNone(calculation)


    def test_delete_calculation(self):
        record_id = add_calculation("add", "10 + 5", 15)

        self.assertTrue(delete_calculation(record_id))
        self.assertFalse(delete_calculation(record_id))

    def test_clear_calculation_history(self):
        add_calculation("add", "2 + 3", 5)
        add_calculation("multiply", "4 * 5", 20)

        deleted = clear_calculation_history()

        self.assertEqual(deleted, 2)
        self.assertEqual(get_calculation_history(), [])

    def test_invalid_history_limit(self):
        with self.assertRaises(ValueError):
            get_calculation_history(0)

        with self.assertRaises(ValueError):
            get_calculation_history(-1)

    # Saved calculation tests

    def test_save_calculation(self):
        record_id = save_calculation(
            "My budget", "5000 + 2500", 7500
        )

        self.assertIsInstance(record_id, int)

    def test_get_saved_calculation(self):
        record_id = save_calculation(
            "My budget", "5000 + 2500", 7500
        )

        saved = get_saved_calculation(record_id)

        self.assertEqual(saved["title"], "My budget")
        self.assertEqual(saved["result"], "7500")

    def test_get_all_saved_calculations(self):
        save_calculation("First", "2 + 3", 5)
        save_calculation("Second", "4 * 5", 20)

        saved = get_saved_calculations()

        self.assertEqual(len(saved), 2)

    def test_delete_saved_calculation(self):
        record_id = save_calculation(
            "Temporary", "10 + 20", 30
        )

        self.assertTrue(delete_saved_calculation(record_id))
        self.assertFalse(delete_saved_calculation(record_id))

    def test_empty_title_validation(self):
        with self.assertRaises(ValueError):
            save_calculation("", "10 + 5", 15)

    def test_empty_expression_validation(self):
        with self.assertRaises(ValueError):
            save_calculation("Test", "", 15)

    def test_missing_result_validation(self):
        with self.assertRaises(ValueError):
            save_calculation("Test", "10 + 5", None)


if __name__ == "__main__":
    unittest.main()
