def compute_total(price: float, quantity: int) -> float:
    subtotal = price * quantity
    tax = subtotal * 0.08
    subtotal += tax
    return subtotal


def swap_two_variables(a, b):
    temp = a
    a = b
    b = temp
    return a, b
