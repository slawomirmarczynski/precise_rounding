import unittest

from precise_rounding.precise_rounding import PreciseRounding


class TestPreciseRounding(unittest.TestCase):

    def test_rounding(self):
        pr = PreciseRounding(123.45678, 0.0215)
        self.assertEqual(pr.value, '123.46')
        self.assertEqual(pr.uncertainty, '0.03')

        pr = PreciseRounding(123.45678, 0.01009)
        self.assertEqual(pr.value, '123.457')
        self.assertEqual(pr.uncertainty, '0.010')

        pr = PreciseRounding(123.4545, 0.07234)
        pr.uncertainty_digits = 2
        self.assertEqual(pr.value, '123.455')
        self.assertEqual(pr.uncertainty, '0.073')

        pr = PreciseRounding(123.4545, 0)
        pr.uncertainty_digits = 2
        self.assertEqual(pr.value, '123.4545')
        self.assertEqual(pr.uncertainty, '0.0000')

    def test_invalid_uncertainty(self):
        with self.assertRaises(ValueError):
            PreciseRounding(123.45678, -0.0215)

    def test_invalid_uncertainty_digits(self):
        with self.assertRaises(ValueError):
            pr = PreciseRounding(123.45678, 0.0215)
            pr.uncertainty_digits = 0

    def test_nan_value(self):
        with self.assertRaises(ValueError):
            PreciseRounding(float('nan'), 0.0215)

    def test_nan_uncertainty(self):
        with self.assertRaises(ValueError):
            PreciseRounding(123.45678, float('nan'))

    def test_exact_uncertainty(self):
        pr = PreciseRounding(123.45678, 0)
        self.assertTrue(pr.is_exact())

    def test_relative_uncertainty(self):
        pr = PreciseRounding(123.45678, 0.0215)
        self.assertAlmostEqual(pr.relative_uncertainty, 0.000174, places=6)


if __name__ == '__main__':
    unittest.main()
