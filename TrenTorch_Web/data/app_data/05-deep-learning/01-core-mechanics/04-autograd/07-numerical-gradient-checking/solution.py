def numerical_gradient(f, x: float, eps: float = 1e-5) -> float:
    return (f(x + eps) - f(x - eps)) / (2 * eps)


def relative_error(analytical: float, numerical: float) -> float:
    denominator = max(abs(analytical), abs(numerical), 1e-12)
    return abs(analytical - numerical) / denominator


def gradient_check(f, x: float, analytical_grad: float, eps: float = 1e-5, tolerance: float = 1e-5) -> bool:
    numerical_grad = numerical_gradient(f, x, eps)
    error = relative_error(analytical_grad, numerical_grad)
    return error < tolerance
