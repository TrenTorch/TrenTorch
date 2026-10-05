def add_backward(grad_output: float) -> tuple[float, float]:
    """
    For z = a + b, given grad_output (dL/dz, the gradient flowing in
    from whatever used z), returns (dL/da, dL/db).

    This starts the "Autograd" track's progressive build: from here on,
    every question builds one more piece toward a minimal, general
    automatic-differentiation engine (Assemble minimal autograd engine),
    starting with the single simplest possible operation's local
    derivative rule.
    """
    pass
