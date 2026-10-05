class InsufficientFundsError(Exception):
    def __init__(self, balance, requested):
        super().__init__(f"balance {balance} is less than {requested}")
        self.balance = balance
        self.requested = requested


def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


def parse_positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError as original:
        raise ValueError(f"not an integer: {text!r}") from original
    if value <= 0:
        raise ValueError(f"not positive: {text!r}")
    return value


def log_and_reraise(func, log: list):
    try:
        return func()
    except Exception as exception:
        log.append(str(exception))
        raise


def check_sorted(values: list) -> None:
    assert all(values[i] <= values[i + 1] for i in range(len(values) - 1)), "not sorted"
