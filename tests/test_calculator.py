import unittest

from calculator import calculate, add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(add(10, 5), 15)

    def test_subtraction(self):
        self.assertEqual(subtract(10, 5), 5)

    def test_multiplication(self):
        self.assertEqual(multiply(10, 5), 50)

    def test_division(self):
        self.assertEqual(divide(10, 5), 2)

    def test_division_by_zero(self):
        self.assertEqual(
            divide(10, 0),
            "Error: Cannot divide by zero"
        )

    def test_invalid_operation(self):
        self.assertEqual(
            calculate("power", 10, 5),
            "Invalid operation"
        )

    def test_calculate_addition(self):
        self.assertEqual(calculate("add", 10, 5), 15)

    def test_calculate_subtraction(self):
        self.assertEqual(calculate("subtract", 10, 5), 5)

    def test_calculate_multiplication(self):
        self.assertEqual(calculate("multiply", 10, 5), 50)

    def test_calculate_division(self):
        self.assertEqual(calculate("divide", 10, 5), 2)


if __name__ == "__main__":
    unittest.main()