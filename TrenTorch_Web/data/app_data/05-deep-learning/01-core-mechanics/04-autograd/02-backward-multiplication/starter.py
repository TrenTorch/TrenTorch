def mul_backward(grad_output: float, a: float, b: float) -> tuple[float, float]:
    """
    For z = a * b, given grad_output (dL/dz), returns (dL/da, dL/db).

    Unlike Backward for addition, multiplication's local derivatives
    depend on the OTHER input's value, this is why mul_backward needs
    both a and b as arguments, not just grad_output.
    """
    pass
