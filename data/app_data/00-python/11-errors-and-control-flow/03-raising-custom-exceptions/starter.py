class InsufficientFundsError(Exception):
    """
    Raised when a withdrawal exceeds the balance.

    __init__(self, balance, requested):
        Call the parent's __init__ (through super()) with the
        message
            f"balance {balance} is less than {requested}"
        and store `balance` and `requested` as attributes.
    """

    def __init__(self, balance, requested):
        pass


def withdraw(balance: float, amount: float) -> float:
    """
    Return balance - amount.
      - If `amount` is not positive (<= 0), raise a ValueError
        with the message "amount must be positive".
      - If `amount` is greater than `balance`, raise
        InsufficientFundsError(balance, amount).
    """
    pass


def parse_positive_int(text: str) -> int:
    """
    Convert `text` to an int with int().
      - If the conversion fails, raise a ValueError with the
        message f"not an integer: {text!r}", CHAINED from the
        original ValueError (use `raise ... from original`).
      - If the number is not positive (<= 0), raise a ValueError
        with the message f"not positive: {text!r}".
    Otherwise return the int.
    """
    pass


def log_and_reraise(func, log: list):
    """
    Call `func()` with no arguments and return its result. If it
    raises any Exception, append str(exception) to `log` and then
    re-raise the SAME exception with a bare `raise`.
    """
    pass


def check_sorted(values: list) -> None:
    """
    Using an assert statement, assert that `values` is in
    non-decreasing order, with the message "not sorted". Return
    nothing when it is sorted.
    """
    pass
