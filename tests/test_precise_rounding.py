import os
import sys
import unittest
from unittest import TestCase

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../precise_rounding')))

from precise_rounding import precise_rounding


class Test(TestCase):

    def test_01(self):
        """oczywiste użycie, domyślna ilość cyfr"""
        supplied = 123.456789, 0.01269
        expected = '123.457', '0.013'
        result = precise_rounding(*supplied)
        self.assertEqual(expected, result)

    def test_02(self):
        """oczywiste użycie, trzy parametry"""
        supplied = 123.456789, 0.01269, 3
        expected = '123.4568', '0.0127'
        result = precise_rounding(*supplied)
        self.assertEqual(expected, result)

    def test_03(self):
        """zerowa niepewność, dwa parametry"""
        supplied = 123.456789, 0
        expected = '123.456789', '0'
        result = precise_rounding(*supplied)
        self.assertEqual(expected, result)

    def test_04(self):
        """zerowa niepewność, trzy parametry"""
        supplied = 123.456789, 0, 4
        expected = '123.456789', '0'
        result = precise_rounding(*supplied)
        self.assertEqual(expected, result)

    def test_05(self):
        """zaokrąglanie wartości"""
        cases = (((123.000, 0.1), ('123.00', '0.10')),
                 ((123.001, 0.1), ('123.00', '0.10')),
                 ((123.002, 0.1), ('123.00', '0.10')),
                 ((123.003, 0.1), ('123.00', '0.10')),
                 ((123.004, 0.1), ('123.00', '0.10')),
                 ((123.005, 0.1), ('123.01', '0.10')),
                 ((123.006, 0.1), ('123.01', '0.10')),
                 ((123.007, 0.1), ('123.01', '0.10')),
                 ((123.008, 0.1), ('123.01', '0.10')),
                 ((123.009, 0.1), ('123.01', '0.10')),
                 ((-123.001, 0.1), ('-123.00', '0.10')),
                 ((-123.002, 0.1), ('-123.00', '0.10')),
                 ((-123.003, 0.1), ('-123.00', '0.10')),
                 ((-123.004, 0.1), ('-123.00', '0.10')),
                 ((-123.005, 0.1), ('-123.01', '0.10')),
                 ((-123.006, 0.1), ('-123.01', '0.10')),
                 ((-123.007, 0.1), ('-123.01', '0.10')),
                 ((-123.008, 0.1), ('-123.01', '0.10')),
                 ((-123.009, 0.1), ('-123.01', '0.10')),)

        for supplied, expected in cases:
            with self.subTest(supplied=supplied):
                result = precise_rounding(*supplied)
                self.assertEqual(expected, result)

    def test_06(self):
        """zaokrąglanie wartości, jedna cyfra znacząca niepewności"""
        cases = (((123.000, 0.01, 1), ('123.00', '0.01')),
                 ((123.001, 0.01, 1), ('123.00', '0.01')),
                 ((123.002, 0.01, 1), ('123.00', '0.01')),
                 ((123.003, 0.01, 1), ('123.00', '0.01')),
                 ((123.004, 0.01, 1), ('123.00', '0.01')),
                 ((123.005, 0.01, 1), ('123.01', '0.01')),
                 ((123.006, 0.01, 1), ('123.01', '0.01')),
                 ((123.007, 0.01, 1), ('123.01', '0.01')),
                 ((123.008, 0.01, 1), ('123.01', '0.01')),
                 ((123.009, 0.01, 1), ('123.01', '0.01')),
                 ((-123.001, 0.01, 1), ('-123.00', '0.01')),
                 ((-123.002, 0.01, 1), ('-123.00', '0.01')),
                 ((-123.003, 0.01, 1), ('-123.00', '0.01')),
                 ((-123.004, 0.01, 1), ('-123.00', '0.01')),
                 ((-123.005, 0.01, 1), ('-123.01', '0.01')),
                 ((-123.006, 0.01, 1), ('-123.01', '0.01')),
                 ((-123.007, 0.01, 1), ('-123.01', '0.01')),
                 ((-123.008, 0.01, 1), ('-123.01', '0.01')),
                 ((-123.009, 0.01, 1), ('-123.01', '0.01')),)

        for supplied, expected in cases:
            with self.subTest(supplied=supplied):
                result = precise_rounding(*supplied)
                self.assertEqual(expected, result)

    def test_07(self):
        """zaokrąglanie wartości, cztery cyfry znaczące niepewności"""
        cases = (((123.000000, 0.01, 4), ('123.00000', '0.01000')),
                 ((123.000001, 0.01, 4), ('123.00000', '0.01000')),
                 ((123.000002, 0.01, 4), ('123.00000', '0.01000')),
                 ((123.000003, 0.01, 4), ('123.00000', '0.01000')),
                 ((123.000004, 0.01, 4), ('123.00000', '0.01000')),
                 ((123.000005, 0.01, 4), ('123.00001', '0.01000')),
                 ((123.000006, 0.01, 4), ('123.00001', '0.01000')),
                 ((123.000007, 0.01, 4), ('123.00001', '0.01000')),
                 ((123.000008, 0.01, 4), ('123.00001', '0.01000')),
                 ((123.000009, 0.01, 4), ('123.00001', '0.01000')),
                 ((-123.000001, 0.01, 4), ('-123.00000', '0.01000')),
                 ((-123.000002, 0.01, 4), ('-123.00000', '0.01000')),
                 ((-123.000003, 0.01, 4), ('-123.00000', '0.01000')),
                 ((-123.000004, 0.01, 4), ('-123.00000', '0.01000')),
                 ((-123.000005, 0.01, 4), ('-123.00001', '0.01000')),
                 ((-123.000006, 0.01, 4), ('-123.00001', '0.01000')),
                 ((-123.000007, 0.01, 4), ('-123.00001', '0.01000')),
                 ((-123.000008, 0.01, 4), ('-123.00001', '0.01000')),
                 ((-123.000009, 0.01, 4), ('-123.00001', '0.01000')),)

        for supplied, expected in cases:
            with self.subTest(supplied=supplied):
                result = precise_rounding(*supplied)
                self.assertEqual(expected, result)

    def test_08(self):
        """zaokrąglanie niepewności w górę"""
        cases = (
            ((123.456789, 0.01234567, 1), ('123.46', '0.02')),
            ((123.456789, 0.01234567, 2), ('123.457', '0.013')),
            ((123.456789, 0.01234567, 3), ('123.4568', '0.0124')),
            ((123.456789, 0.01234567, 4), ('123.45679', '0.01235')),
            ((123.456789, 0.01234567, 5), ('123.456789', '0.012346')),
            ((123.456789, 0.01234567, 6), ('123.4567890', '0.0123457')),
            ((123.456789, 0.01234567, 7), ('123.45678900', '0.01234567')),
            ((123.456789, 0.01234567, 8), ('123.456789000', '0.012345670')),
            ((123.456789, 0.01234567, 9), ('123.4567890000', '0.0123456700')),
        )

        for supplied, expected in cases:
            with self.subTest(supplied=supplied):
                result = precise_rounding(*supplied)
                self.assertEqual(expected, result)

    def test_09(self):
        """zaokrąglanie niepewności w dół"""
        cases = (
            ((123.456789, 0.010234567, 1), ('123.46', '0.01')),
            ((123.456789, 0.012034567, 2), ('123.457', '0.012')),
            ((123.456789, 0.012304567, 3), ('123.4568', '0.0123')),
            ((123.456789, 0.012340567, 4), ('123.45679', '0.01234')),
            ((123.456789, 0.012345067, 5), ('123.456789', '0.012345')),
            ((123.456789, 0.012345607, 6), ('123.4567890', '0.0123456')),
            ((123.456789, 0.012345670, 7), ('123.45678900', '0.01234567')),
        )

        for supplied, expected in cases:
            with self.subTest(supplied=supplied):
                result = precise_rounding(*supplied)
                self.assertEqual(expected, result)

    def test_exceptions(self):
        """testowanie wyjątków"""

        cases = ((('abc', 0.01), TypeError), ((10.0, 'abc'), TypeError),
                 ((1.0, 0.01, 'abc'), TypeError), ((1.0, -0.01), ValueError),
                 ((1.0, 0.01, 0), ValueError), ((1.0, 0.01, -1), ValueError))

        for parameters, exception in cases:
            with self.subTest(parameters=parameters):
                with self.assertRaises(exception):
                    precise_rounding(*parameters)


if __name__ == '__main__':
    unittest.main()
