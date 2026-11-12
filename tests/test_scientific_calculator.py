import unittest
import math

from scientific_calculator import (
    power,
    square_root,
    logarithm,
    sine,
    cosine,
    tangent,
    get_constant
)


class TestScientificCalculator(unittest.TestCase):

    def test_power(self):
        self.assertEqual(power(2, 3), 8)

    def test_square_root(self):
        self.assertEqual(square_root(25), 5)

    def test_negative_square_root(self):
        self.assertEqual(
            square_root(-25),
            "Error: Cannot calculate square root of a negative number"
        )

    def test_logarithm(self):
        self.assertAlmostEqual(logarithm(100), 2)

    def test_invalid_logarithm_number(self):
        self.assertIn("Error", logarithm(-10))

    def test_invalid_logarithm_base(self):
        self.assertIn("Error", logarithm(100, 1))

    def test_sine(self):
        self.assertAlmostEqual(sine(30), 0.5)

    def test_cosine(self):
        self.assertAlmostEqual(cosine(60), 0.5)

    def test_tangent(self):
        self.assertAlmostEqual(tangent(45), 1)

    def test_undefined_tangent(self):
        self.assertIn("Error", tangent(90))

    def test_pi_constant(self):
        self.assertEqual(get_constant("pi"), math.pi)

    def test_e_constant(self):
        self.assertEqual(get_constant("e"), math.e)

    def test_invalid_constant(self):
        self.assertEqual(
            get_constant("unknown"),
            "Invalid constant"
        )


if __name__ == "__main__":
    unittest.main()
