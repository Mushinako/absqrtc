""""""
from typing import NoReturn


def raise_duplicate_arg_error(func_name: str, arg_name: str) -> NoReturn:
    """"""
    raise TypeError(f"{func_name}() got multiple values for argument {arg_name!r}")


def raise_missing_arg_error(func_name: str, arg_name: str) -> NoReturn:
    raise TypeError(f"{func_name}() missing positional argument: {arg_name!r}")
