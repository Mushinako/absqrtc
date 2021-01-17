from fractions import Fraction
from math import sqrt

import pytest

from absqrtc import ABSqrtC


class TestInstance:
    def test_construction(self):
        with pytest.raises(ValueError):
            ABSqrtC(0, 0, 0)

        with pytest.raises(ValueError):
            ABSqrtC(-1, -1, -1)

        ABSqrtC(0, 0, 1)

    def test_reduction(self):
        t1 = ABSqrtC(0, 75)
        assert t1.add == 0
        assert t1.factor == 5
        assert t1.radical == 3

        t2 = ABSqrtC(3, -5, 98)
        assert t2.add == 3
        assert t2.factor == -35
        assert t2.radical == 2

        t3 = ABSqrtC(-5, 3, 9)
        assert t3.add == 4
        assert t3.factor == 0
        assert t3.radical == 1

        t4 = ABSqrtC(-3, 0, 200)
        assert t4.add == -3
        assert t4.factor == 0
        assert t4.radical == 1

    def test_value(self):
        assert ABSqrtC(1, 1, 1).value == 2
        assert ABSqrtC(3, -5, 7).value == 3 - 5 * sqrt(7)

    def test_bool(self):
        assert not bool(ABSqrtC(0, 0, 1))
        assert bool(ABSqrtC(1, 1, 1))

    def test_str(self):
        assert str(ABSqrtC(1, 0, 1)) == "1"
        assert str(ABSqrtC(1, 1, 2)) == "1 + √2"
        assert str(ABSqrtC(1, 2, 2)) == "1 + 2 * √2"
        assert str(ABSqrtC(-1, -2, 2)) == "-1 - 2 * √2"
        assert str(ABSqrtC(Fraction(1, 2), Fraction(1, 2), 2)) == "1/2 + 1/2 * √2"


class TestComparisons:
    def test_eq(self):
        assert ABSqrtC(3, 5, 7) == ABSqrtC(3, 5, 7)
        assert ABSqrtC(3, 5, 7) == ABSqrtC(3, 1, 175)

    def test_ne(self):
        assert ABSqrtC(3, 5, 7) != ABSqrtC(3, 5, 8)

    def test_lt(self):
        assert ABSqrtC(3, 5, 7) < ABSqrtC(3, 5, 8)
        assert ABSqrtC(3, 5, 7) < ABSqrtC(3, 6, 7)
        assert ABSqrtC(3, 5, 7) < ABSqrtC(4, 5, 7)

    def test_le(self):
        assert ABSqrtC(3, 5, 7) <= ABSqrtC(3, 5, 8)
        assert ABSqrtC(3, 5, 7) <= ABSqrtC(3, 6, 7)
        assert ABSqrtC(3, 5, 7) <= ABSqrtC(4, 5, 7)
        assert ABSqrtC(3, 5, 7) <= ABSqrtC(3, 5, 7)

    def test_gt(self):
        assert ABSqrtC(3, 5, 7) > ABSqrtC(3, 5, 6)
        assert ABSqrtC(3, 5, 7) > ABSqrtC(3, 4, 7)
        assert ABSqrtC(3, 5, 7) > ABSqrtC(2, 5, 7)

    def test_ge(self):
        assert ABSqrtC(3, 5, 7) >= ABSqrtC(3, 5, 6)
        assert ABSqrtC(3, 5, 7) >= ABSqrtC(3, 4, 7)
        assert ABSqrtC(3, 5, 7) >= ABSqrtC(2, 5, 7)
        assert ABSqrtC(3, 5, 7) >= ABSqrtC(3, 5, 7)


class TestCalculationsBinary:
    def test_add(self):
        t1 = ABSqrtC(2, 0, 1)
        t2 = ABSqrtC(3, -5, 7)
        t3 = ABSqrtC(3, 5, 7)
        t4 = ABSqrtC(3, 10, 7)
        t5 = ABSqrtC(3, 5, 11)

        with pytest.raises(ValueError):
            t2 + t5

        assert t1 + t3 == ABSqrtC(5, 5, 7)
        assert t2 + t3 == ABSqrtC(6, 0, 1)
        assert t2 + t4 == ABSqrtC(6, 5, 7)

    def test_sub(self):
        t1 = ABSqrtC(2, 0, 1)
        t2 = ABSqrtC(3, -5, 7)
        t3 = ABSqrtC(3, 5, 7)
        t4 = ABSqrtC(2, -10, 7)
        t5 = ABSqrtC(3, 5, 11)

        with pytest.raises(ValueError):
            t2 - t5

        assert t1 - t1 == ABSqrtC(0, 0, 1)
        assert t1 - t3 == ABSqrtC(-1, -5, 7)
        assert t2 - t3 == ABSqrtC(0, -10, 7)
        assert t2 - t4 == ABSqrtC(1, 5, 7)

    def test_mul(self):
        t1 = ABSqrtC(2, 0, 1)
        t2 = ABSqrtC(3, -5, 7)
        t3 = ABSqrtC(3, 5, 7)
        t4 = ABSqrtC(2, 10, 7)
        t5 = ABSqrtC(3, 5, 11)

        with pytest.raises(ValueError):
            t2 * t5

        assert t1 * t1 == ABSqrtC(4, 0, 1)
        assert t1 * t3 == ABSqrtC(6, 10, 7)
        assert t2 * t3 == ABSqrtC(-166, 0, 1)
        assert t2 * t4 == ABSqrtC(-344, 20, 7)

    def test_truediv(self):
        t1 = ABSqrtC(2, 0, 1)
        t2 = ABSqrtC(3, -5, 7)
        t3 = ABSqrtC(3, 5, 7)
        t4 = ABSqrtC(2, 10, 7)
        t5 = ABSqrtC(3, 5, 11)

        with pytest.raises(ValueError):
            t2 / t5

        assert t1 / t1 == ABSqrtC(1, 0, 1)
        assert t2 / t1 == ABSqrtC(Fraction(3, 2), Fraction(-5, 2), 7)
        assert t1 / t3 == ABSqrtC(Fraction(-3, 83), Fraction(5, 83), 7)
        assert t2 / t3 == ABSqrtC(Fraction(-92, 83), Fraction(15, 83), 7)
        assert t2 / t4 == ABSqrtC(Fraction(-89, 174), Fraction(5, 87), 7)

    def test_pow(self):
        t1 = ABSqrtC(-1, 1, 2)

        assert t1 ** 2 == ABSqrtC(3, -2, 2)
        assert t1 ** 3 == ABSqrtC(-7, 5, 2)
        assert t1 ** 5 == ABSqrtC(-41, 29, 2)
        assert t1 ** 10 == ABSqrtC(3363, -2378, 2)


class TestCalculationsUnary:
    def test_neg(self):
        assert -ABSqrtC(1, 1, 2) == ABSqrtC(-1, -1, 2)

    def test_abs(self):
        assert abs(ABSqrtC(2, -1, 2)) == ABSqrtC(2, -1, 2)
        assert abs(ABSqrtC(1, -1, 2)) == ABSqrtC(-1, 1, 2)

    def test_invert_conjugate(self):
        t1 = ABSqrtC(1, 1, 2)

        assert ~t1 == t1.conjugate() == ABSqrtC(1, -1, 2)