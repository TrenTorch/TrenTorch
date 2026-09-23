def mul_backward(grad_output: float, a: float, b: float) -> tuple[float, float]:
    grad_a = grad_output * b
    grad_b = grad_output * a
    return grad_a, grad_b
