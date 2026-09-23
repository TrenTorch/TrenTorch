def receipt_line(item: str, qty: int, price: float) -> str:
    return f"{item:<12}{qty:>4}{price:>10.2f}"


def format_percent(value: float, decimals: int) -> str:
    return f"{value:.{decimals}%}"


def format_binary(n: int, width: int) -> str:
    return f"{n:0{width}b}"


def debug_label(label: str, value) -> str:
    return f"{label}={value!r}"
