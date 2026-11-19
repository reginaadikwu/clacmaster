
from database import get_connection


def add_calculation(operation, expression, result):
    """Save a calculation to the history table."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO calculation_history
            (operation, expression, result)
            VALUES (?, ?, ?)
            """,
            (operation, expression, str(result))
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_calculation_history(limit=50):
    """Retrieve the most recent calculations."""

    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("Limit must be a positive integer")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM calculation_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_calculation_by_id(calculation_id):
    """Retrieve one calculation from history using its ID."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM calculation_history
            WHERE id = ?
            """,
            (calculation_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def delete_calculation(calculation_id):
    """Delete one calculation using its ID."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM calculation_history WHERE id = ?",
            (calculation_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def clear_calculation_history():
    """Delete all calculation history."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM calculation_history")

        deleted_count = cursor.rowcount

        connection.commit()

        return deleted_count

    finally:
        connection.close()
