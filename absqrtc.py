"""
Module: `a + b sqrt(c)` object
"""

from __future__ import annotations

from fractions import Fraction
from functools import total_ordering
from math import ceil, floor, sqrt, trunc
from typing import overload


@total_ordering
class ABSqrtC:
    """
    `a + b sqrt(c)` object
    """

    def __init__(self, a: Fraction, b: Fraction, c: int) -> None:
        if c < 0:
            raise ValueError(f"Negative {c=} not yet supported")

        extra_square, c_remainder = _get_square_factors(c)

        if c_remainder == 1:
            a += b * extra_square
            self._factor = _FactorFraction(0)
            self._radical = 1
        else:
            self._factor = _FactorFraction(b * extra_square)
            self._radical = c_remainder

        self._add = _AddFraction(a)

        self._value = a + b * sqrt(c)

    @property
    def add(self) -> Fraction:
        return self._add

    @property
    def factor(self) -> Fraction:
        return self._factor

    @property
    def radical(self) -> int:
        return self._radical

    @property
    def value(self) -> float:
        return self._value

    def __str__(self) -> str:
        string = str(self._add)

        if not self._factor:
            return string

        string += f" + " if self._factor > 0 else f" - "

        if (abs_factor := abs(self._factor)) != 1:
            string += f"{abs_factor} * "

        return string + f"√{self._radical}"

    def __repr__(self) -> str:
        return f"ASqrtB({self.__str__()})"

    def __eq__(self, other: ABSqrtC) -> bool:
        return (
            self._add == other._add
            and self._factor == other._factor
            and self._radical == other._radical
        )

    def __lt__(self, other: ABSqrtC) -> bool:
        return self._value < other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return bool(self._value)

    def __add__(self, other: ABSqrtC) -> ABSqrtC:
        radical = self._get_common_radical(other)
        return ABSqrtC(self._add + other._add, self._factor + other._factor, radical)

    def __sub__(self, other: ABSqrtC) -> ABSqrtC:
        radical = self._get_common_radical(other)
        return ABSqrtC(self._add - other._add, self._factor - other.factor, radical)

    def __mul__(self, other: ABSqrtC) -> ABSqrtC:
        radical = self._get_common_radical(other)
        return ABSqrtC(
            self._mul_add(other._add, other._factor, radical),
            self._mul_factor(other._add, other._factor),
            radical,
        )

    def __truediv__(self, other: ABSqrtC) -> ABSqrtC:
        radical = self._get_common_radical(other)
        denominator = other._mul_add(other._add, -other._factor, other._radical)
        return ABSqrtC(
            self._mul_add(other._add, -other._factor, radical) / denominator,
            self._mul_factor(other._add, -other._factor) / denominator,
            radical,
        )

    def __pow__(self, power: int) -> ABSqrtC:
        add = self._add
        factor = self._factor

        for _ in range(power - 1):
            add, factor = (
                self._mul_add(add, factor, self._radical),
                self._mul_factor(add, factor),
            )

        return ABSqrtC(add, factor, self._radical)

    def __neg__(self) -> ABSqrtC:
        return ABSqrtC(-self._add, -self._factor, self._radical)

    def __abs__(self) -> ABSqrtC:
        return self if self._value >= 0 else -self

    def __invert__(self) -> ABSqrtC:
        return self.conjugate()

    def __complex__(self) -> complex:
        return complex(self._value)

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> float:
        return self._value

    @overload
    def __round__(self) -> int:
        ...

    @overload
    def __round__(self, ndigits: None) -> int:
        ...

    @overload
    def __round__(self, ndigits: int) -> float:
        ...

    def __round__(self, ndigits=None):  # type: ignore
        return round(self._value, ndigits)  # type: ignore

    def __trunc__(self) -> int:
        return trunc(self._value)

    def __floor__(self) -> int:
        return floor(self._value)

    def __ceil__(self) -> int:
        return ceil(self._value)

    def conjugate(self) -> ABSqrtC:
        """
        Get the radical conjugate
        """
        return ABSqrtC(self._add, -self._factor, self._radical)

    def _get_common_radical(self, other: ABSqrtC) -> int:
        """
        Get common radicals of 2 ABSqrtC numbers
        """
        if self._radical == 1:
            return other._radical
        if other._radical == 1:
            return self._radical
        if self._radical == other._radical:
            return self._radical
        raise ValueError(
            f"Add different radicals ({self._radical} and {other._radical}) not yet supported"
        )

    def _mul_add(
        self, other_add: _AddFraction, other_factor: _FactorFraction, radical: int
    ) -> _AddFraction:
        """
        Get the addition part of the multiplied number
        """
        return _AddFraction(
            self._add * other_add + self._factor * other_factor * radical
        )

    def _mul_factor(
        self, other_add: _AddFraction, other_factor: _FactorFraction
    ) -> _FactorFraction:
        """
        Get the factor part of the multiplied number
        """
        return _FactorFraction(self._add * other_factor + self._factor * other_add)


class _BeauFraction(Fraction):
    """
    Beautiful fraction, with proper `__str__`
    """

    def __str__(self) -> str:
        string = ""
        if self < 0:
            string += "- "

        abs_self = abs(self)

        string += f"{abs_self.numerator}"

        if (denominator := abs_self.denominator) > 1:
            string += f" / {denominator}"

        return string


class _AddFraction(_BeauFraction):
    """
    Fraction for addition part, mainly for type annotation
    """


class _FactorFraction(_BeauFraction):
    """
    Fraction for factor part, mainly for type annotation
    """

    def __neg__(self) -> _FactorFraction:
        return _FactorFraction(super().__neg__())


def _get_square_factors(n: int) -> tuple[int, int]:
    """
    Separate all square factors of the number
    """
    square_factor: int = 1

    for i in range(2, int(n ** 0.25)):
        if not n % (square := i * i):
            square_factor *= i
            n //= square

    return square_factor, n
