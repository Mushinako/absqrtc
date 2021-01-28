"""
Module: `a + b sqrt(c)` object
"""

from __future__ import annotations

from decimal import Decimal as D
from fractions import Fraction as F
from functools import cached_property
from itertools import count
from math import comb, sqrt
from numbers import Real
from typing import Optional, Union, overload


class ABSqrtC:
    """
    `a + b sqrt(c)` object
    """

    _cache: dict[tuple[F, F, int], ABSqrtC] = {}

    def __new__(
        cls,
        a: _InputTypesUnion,
        bc: Optional[_InputTypesUnion] = None,
        c: Optional[_InputTypesUnion] = None,
        /,
    ) -> ABSqrtC:
        frac_a = a if isinstance(a, F) else F(a)

        if bc is None:
            frac_b = F(0)
            frac_c = F(1)
        elif c is None:
            frac_b = F(1)
            frac_c = bc if isinstance(bc, F) else F(bc)
        else:
            frac_b = bc if isinstance(bc, F) else F(bc)
            frac_c = F(1) if not frac_b else c if isinstance(c, F) else F(c)

        if frac_c < 0:
            raise ValueError(f"Negative radical {frac_c} not yet supported")
        elif not frac_c:
            frac_c = F(1)

        b_mul, c = _get_square_factors(frac_c)
        if c == 1:
            frac_a += frac_b * b_mul
            frac_b = F(0)
        else:
            frac_b *= b_mul

        if (n := cls._cache.get((frac_a, frac_b, c))) is None:
            obj: cls = super().__new__(cls)
            obj._init(frac_a, frac_b, c)
            cls._cache[frac_a, frac_b, c] = obj
            return obj
        else:
            return n

    def _init(self, a: F, b: F, c: int) -> None:
        self._add = a
        self._factor = b
        self._radical = c

        self._value = a + b * sqrt(c)
        self._conjugate_product = a * a - b * b * c

        self._factor_abs = abs(b)

    @property
    def add(self) -> F:
        return self._add

    @property
    def factor(self) -> F:
        return self._factor

    @property
    def radical(self) -> int:
        return self._radical

    @property
    def value(self) -> float:
        return self._value

    @property
    def conjugate_product(self) -> F:
        """
        Product with its radical conjugate
        """
        return self._conjugate_product

    @cached_property
    def conjugate(self) -> ABSqrtC:
        """
        Its radical conjugate
        """
        return ABSqrtC(self._add, -self._factor, self._radical)

    @cached_property
    def inverse(self) -> ABSqrtC:
        """
        Its multiplicative inverse (1/self)
        """
        return ABSqrtC(
            self._add / self._conjugate_product,
            -self._factor / self._conjugate_product,
            self._radical,
        )

    def __del__(self) -> None:
        type(self)._cache.pop((self._add, self._factor, self._radical), None)

    def __str__(self) -> str:
        if not self._factor:
            return f"{self._add or 0}"

        if self._add:
            string = f"{self._add} {'+' if self._factor > 0 else '-'} "
        else:
            string = "" if self._factor > 0 else "-"

        if self._factor_abs != 1:
            string += f"{self._factor_abs} * "

        return string + f"√{self._radical}"

    def __repr__(self) -> str:
        return f"ABSqrtC({self})"

    def __format__(self, format_spec: str) -> str:
        return self._value.__format__(format_spec)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ABSqrtC):
            return (
                self._add == o._add
                and self._factor == o._factor
                and self._radical == o._radical
            )
        if isinstance(o, Real):
            return self._value == o
        return NotImplemented

    def __ne__(self, o: object) -> bool:
        if isinstance(o, ABSqrtC):
            return (
                self._add != o._add
                or self._factor != o._factor
                or self._radical != o._radical
            )
        if isinstance(o, Real):
            return self._value != o
        return NotImplemented

    def __lt__(self, o: object) -> bool:
        if isinstance(o, ABSqrtC):
            return self._value < o._value
        if isinstance(o, Real):
            return self._value < float(o)
        return NotImplemented

    def __le__(self, o: object) -> bool:
        if isinstance(o, ABSqrtC):
            return self._value <= o._value
        if isinstance(o, Real):
            return self._value <= float(o)
        return NotImplemented

    def __gt__(self, o: object) -> bool:
        if isinstance(o, ABSqrtC):
            return self._value > o._value
        if isinstance(o, Real):
            return self._value > float(o)
        return NotImplemented

    def __ge__(self, o: object) -> bool:
        if isinstance(o, ABSqrtC):
            return self._value >= o._value
        if isinstance(o, Real):
            return self._value >= float(o)
        return NotImplemented

    def __hash__(self) -> int:
        return self._value.__hash__()

    def __bool__(self) -> bool:
        return self._value.__bool__()

    def __add__(self, o: object) -> ABSqrtC:
        if isinstance(o, ABSqrtC):
            radical = self.get_common_radical(o)
            return ABSqrtC(self._add + o._add, self._factor + o._factor, radical)
        if isinstance(o, _NumTypes):
            return ABSqrtC(
                self._add + (o if isinstance(o, F) else F(o)),
                self._factor,
                self._radical,
            )
        return NotImplemented

    def __radd__(self, o: object) -> ABSqrtC:
        if isinstance(o, ABSqrtC):
            radical = o.get_common_radical(self)
            return ABSqrtC(o._add + self._add, o._factor + self._factor, radical)
        if isinstance(o, _NumTypes):
            return ABSqrtC(
                (o if isinstance(o, F) else F(o)) + self._add,
                self._factor,
                self._radical,
            )
        return NotImplemented

    def __sub__(self, o: object) -> ABSqrtC:
        if isinstance(o, ABSqrtC):
            radical = self.get_common_radical(o)
            return ABSqrtC(self._add - o._add, self._factor - o._factor, radical)
        if isinstance(o, _NumTypes):
            return ABSqrtC(
                self._add - (o if isinstance(o, F) else F(o)),
                self._factor,
                self._radical,
            )
        return NotImplemented

    def __rsub__(self, o: object) -> ABSqrtC:
        if isinstance(o, ABSqrtC):
            radical = o.get_common_radical(self)
            return ABSqrtC(o._add - self._add, o._factor - self._factor, radical)
        if isinstance(o, _NumTypes):
            return ABSqrtC(
                (o if isinstance(o, F) else F(o)) - self._add,
                -self._factor,
                self._radical,
            )
        return NotImplemented

    def __mul__(self, o: object) -> ABSqrtC:
        if isinstance(o, ABSqrtC):
            radical = self.get_common_radical(o)
            return ABSqrtC(
                self._add * o._add + self._factor * o._factor * radical,
                self._add * o._factor + self._factor * o._add,
                radical,
            )
        if isinstance(o, _NumTypes):
            f_o = o if isinstance(o, F) else F(o)
            return ABSqrtC(self._add * f_o, self._factor * f_o, self._radical)
        return NotImplemented

    def __rmul__(self, o: object) -> ABSqrtC:
        if isinstance(o, ABSqrtC):
            radical = o.get_common_radical(self)
            return ABSqrtC(
                o._add * self._add + o._factor * self._factor * radical,
                o._add * self._factor + o._factor * self._add,
                radical,
            )
        if isinstance(o, _NumTypes):
            f_o = o if isinstance(o, F) else F(o)
            return ABSqrtC(f_o * self._add, f_o * self._factor, self._radical)
        return NotImplemented

    def __truediv__(self, o: object) -> ABSqrtC:
        if isinstance(o, ABSqrtC):
            radical = self.get_common_radical(o)
            return ABSqrtC(
                (self._add * o._add - self._factor * o._factor * radical)
                / o._conjugate_product,
                (self._factor * o._add - self._add * o._factor) / o._conjugate_product,
                radical,
            )
        if isinstance(o, _NumTypes):
            f_o = o if isinstance(o, F) else F(o)
            return ABSqrtC(self._add / f_o, self._factor / f_o, self._radical)
        return NotImplemented

    def __rtruediv__(self, o: object) -> ABSqrtC:
        if isinstance(o, ABSqrtC):
            radical = o.get_common_radical(self)
            return ABSqrtC(
                (o._add * self._add - o._factor * self._factor * radical)
                / self._conjugate_product,
                (o._factor * self._add - o._add * self._factor)
                / self._conjugate_product,
                radical,
            )
        if isinstance(o, _NumTypes):
            factor = (o if isinstance(o, F) else F(o)) / self._conjugate_product
            return ABSqrtC(factor * self._add, -factor * self._factor, self._radical)
        return NotImplemented

    def __pow__(self, o: object) -> ABSqrtC:
        if isinstance(o, int):
            a = self._add
            b = self._factor
            c = self._radical
            add = F(0)
            factor = F(0)
            for i in range(0, o, 2):
                add += comb(o, i) * a ** (o - i) * b ** i * c ** (i // 2)
                i += 1
                factor += comb(o, i) * a ** (o - i) * b ** i * c ** (i // 2)
            if not o % 2:
                add += b ** o * c ** (o // 2)
            return ABSqrtC(add, factor, self._radical)
        return NotImplemented

    def __pos__(self) -> ABSqrtC:
        return self

    def __neg__(self) -> ABSqrtC:
        return ABSqrtC(-self._add, -self._factor, self._radical)

    def __abs__(self) -> ABSqrtC:
        return (
            self
            if self._value >= 0
            else ABSqrtC(-self._add, -self._factor, self._radical)
        )

    def __invert__(self) -> ABSqrtC:
        return ABSqrtC(self._add, -self._factor, self._radical)

    def __complex__(self) -> complex:
        return self._value + 0j

    def __float__(self) -> float:
        return self._value

    def __int__(self) -> int:
        return self._value.__int__()

    @overload
    def __round__(self, ndigits: None = ...) -> int:
        ...

    @overload
    def __round__(self, ndigits: int) -> float:
        ...

    def __round__(self, ndigits: Optional[int] = None) -> Union[int, float]:
        return self._value.__round__(ndigits)

    def __trunc__(self) -> int:
        return self._value.__trunc__()

    def __floor__(self) -> int:
        return self._value.__floor__()

    def __ceil__(self) -> int:
        return self._value.__ceil__()

    def get_common_radical(self, o: ABSqrtC) -> int:
        """
        Get common radicals of 2 ABSqrtC numbers
        """
        if self._radical == o._radical:
            return self._radical
        if self._radical == 1:
            return o._radical
        if o._radical == 1:
            return self._radical
        raise ValueError(
            f"Different radicals ({self._radical} and {o._radical}) not yet supported"
        )


def _get_square_factors(n: F) -> tuple[F, int]:
    """
    Separate all square factors of the number
    """
    square_factor = F(1, n.denominator)
    n_int = n.numerator * n.denominator

    for i in count(2):
        square = i * i
        if square > n:
            break
        while not n_int % square:
            square_factor *= i
            n_int //= square

    return square_factor, n_int


_NumTypes = (D, F, int, str)
_InputTypesUnion = Union[D, F, int, str]
