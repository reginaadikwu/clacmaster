import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database
from web.app import app


class TestCalcMasterWeb(unittest.TestCase):

    def setUp(self):
        # Give every test its own temporary database
        self.temp_dir = tempfile.TemporaryDirectory()
        temp_path = Path(self.temp_dir.name)

        self.data_patch = patch.object(
            database, "DATA_DIR", temp_path
        )
        self.database_patch = patch.object(
            database, "DATABASE_PATH", temp_path / "test.db"
        )

        self.data_patch.start()
        self.database_patch.start()

        database.initialize_database()

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        self.database_patch.stop()
        self.data_patch.stop()
        self.temp_dir.cleanup()

    def test_home_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CalcMaster", response.data)

    def test_successful_calculation_is_saved_to_history(self):
        response = self.client.post("/", data={
            "operation": "add",
            "number": "10",
            "second_number": "5"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"15.0", response.data)

        from history import get_calculation_history

        history = get_calculation_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["expression"], "10.0 + 5.0")

    def test_division_by_zero_is_not_saved(self):
        response = self.client.post("/", data={
            "operation": "divide",
            "number": "10",
            "second_number": "0"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Error:", response.data)

        from history import get_calculation_history

        self.assertEqual(get_calculation_history(), [])

    def test_save_calculation_route(self):
        from history import add_calculation
        from saved_calculations import get_saved_calculations

        calculation_id = add_calculation("add", "10 + 5", 15)

        response = self.client.post("/saved", data={
            "title": "My Test",
            "calculation_id": str(calculation_id)
        })

        self.assertEqual(response.status_code, 302)

        saved = get_saved_calculations()

        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["title"], "My Test")
        self.assertEqual(saved[0]["expression"], "10 + 5")
        self.assertEqual(saved[0]["result"], "15")

    def test_save_nonexistent_calculation_is_rejected(self):
        from saved_calculations import get_saved_calculations

        response = self.client.post("/saved", data={
            "title": "Invalid Calculation",
            "calculation_id": "9999"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_saved_calculations(), [])

    def test_browser_submitted_expression_and_result_are_ignored(self):
        from history import add_calculation
        from saved_calculations import get_saved_calculations

        calculation_id = add_calculation("add", "10 + 5", 15)

        self.client.post("/saved", data={
            "title": "Trusted Calculation",
            "calculation_id": str(calculation_id),
            "expresssssion": "999 + 999",
            "result": "1998"
        })

        saved = get_saved_calculations()

        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["expression"], "10 + 5")
        self.assertEqual(saved[0]["result"], "15")
    
    def test_delete_history_route(self):
        from history import add_calculation, get_calculation_history

        record_id = add_calculation("add", "2 + 3", 5)

        response = self.client.post(
            f"/history/{record_id}/delete"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_calculation_history(), [])

    def test_clear_history_route(self):
        from history import add_calculation, get_calculation_history

        add_calculation("add", "2 + 3", 5)
        add_calculation("multiply", "4 * 5", 20)

        response = self.client.post("/history/clear")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_calculation_history(), [])

    def test_delete_saved_calculation_route(self):
        from saved_calculations import (
            save_calculation,
            get_saved_calculations
        )

        record_id = save_calculation("Temporary", "10 + 5", 15)

        response = self.client.post(
            f"/saved/{record_id}/delete"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_saved_calculations(), [])


if __name__ == "__main__":
    unittest.main()
