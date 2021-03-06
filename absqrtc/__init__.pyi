from __future__ import annotations

from decimal import Decimal as D
from fractions import Fraction as F
from functools import cached_property
from numbers import Real
from typing import Union, overload

class ABSqrtC:
    _cache: dict[tuple[F, F, int], ABSqrtC]
    @overload
    def __new__(cls, a: _InputType, /) -> ABSqrtC: ...
    @overload
    def __new__(cls, a: _InputType, c: _InputType, /) -> ABSqrtC: ...
    @overload
    def __new__(cls, a: _InputType, b: _InputType, c: _InputType, /) -> ABSqrtC: ...
    def _init(self, a: F, b: F, c: int) -> None: ...
    @property
    def add(self) -> F: ...
    @property
    def factor(self) -> F: ...
    @property
    def radical(self) -> int: ...
    @property
    def value(self) -> float: ...
    @property
    def conjugate_product(self) -> F: ...
    @cached_property
    def conjugate(self) -> ABSqrtC: ...
    @cached_property
    def inverse(self) -> ABSqrtC: ...
    def __del__(self) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __format__(self, format_spec: str) -> str: ...
    def __eq__(self, o: _ComparisonType) -> bool: ...
    def __ne__(self, o: _ComparisonType) -> bool: ...
    def __lt__(self, o: _ComparisonType) -> bool: ...
    def __le__(self, o: _ComparisonType) -> bool: ...
    def __gt__(self, o: _ComparisonType) -> bool: ...
    def __ge__(self, o: _ComparisonType) -> bool: ...
    def __hash__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __add__(self, o: _ArithmaticType) -> ABSqrtC: ...
    def __radd__(self, o: _ArithmaticType) -> ABSqrtC: ...
    def __sub__(self, o: _ArithmaticType) -> ABSqrtC: ...
    def __rsub__(self, o: _ArithmaticType) -> ABSqrtC: ...
    def __mul__(self, o: _ArithmaticType) -> ABSqrtC: ...
    def __rmul__(self, o: _ArithmaticType) -> ABSqrtC: ...
    def __truediv__(self, o: _ArithmaticType) -> ABSqrtC: ...
    def __rtruediv__(self, o: _ArithmaticType) -> ABSqrtC: ...
    def __pow__(self, o: int) -> ABSqrtC: ...
    def __pos__(self) -> ABSqrtC: ...
    def __neg__(self) -> ABSqrtC: ...
    def __abs__(self) -> ABSqrtC: ...
    def __invert__(self) -> ABSqrtC: ...
    def __complex__(self) -> complex: ...
    def __float__(self) -> float: ...
    def __int__(self) -> int: ...
    @overload
    def __round__(self, ndigits: None = ...) -> int: ...
    @overload
    def __round__(self, ndigits: int) -> float: ...
    def __trunc__(self) -> int: ...
    def __floor__(self) -> int: ...
    def __ceil__(self) -> int: ...
    def get_common_radical(self, o: ABSqrtC) -> int: ...

_InputType = Union[D, F, int, str]
_ComparisonType = Union[ABSqrtC, Real]
_ArithmaticType = Union[ABSqrtC, D, F, int, str]
