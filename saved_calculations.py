
from database import get_connection


def save_calculation(title, expression, result):
    """Save a calculation with a user-provided title."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be empty")

    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Expression cannot be empty")

    if result is None:
        raise ValueError("Result cannot be empty")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO saved_calculations
            (title, expression, result)
            VALUES (?, ?, ?)
            """,
            (title.strip(), expression.strip(), str(result))
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_saved_calculations():
    """Retrieve all saved calculations."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM saved_calculations
            ORDER BY id DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_saved_calculation(calculation_id):
    """Retrieve one saved calculation by its ID."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM saved_calculations
            WHERE id = ?
            """,
            (calculation_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def delete_saved_calculation(calculation_id):
    """Delete one saved calculation."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM saved_calculations
            WHERE id = ?
            """,
            (calculation_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()
