def numerical_gradient(f, x: float, eps: float = 1e-5) -> float:
    """
    `01-derivatives-first-principles`'s own central difference formula
    (Math & Statistics), the ground-truth approximation every
    analytical gradient in this curriculum, `Assemble minimal autograd
    engine`'s included, gets checked against.

        f'(x) ~= (f(x + eps) - f(x - eps)) / (2 * eps)
    """
    pass


def relative_error(analytical: float, numerical: float) -> float:
    """
    Compares two gradient estimates in a way that's robust to their
    overall SCALE: an absolute difference of 0.001 is huge when both
    gradients are around 0.0001, but negligible when both are around
    1000. Dividing by the larger of the two magnitudes (floored at a
    tiny constant, to avoid dividing by zero when both are exactly 0)
    normalizes for this.

        relative_error = |analytical - numerical| / max(|analytical|, |numerical|, 1e-12)
    """
    pass


def gradient_check(f, x: float, analytical_grad: float, eps: float = 1e-5, tolerance: float = 1e-5) -> bool:
    """
    The capstone of this entire track, and the exact discipline every
    hand-derived backward pass in this curriculum has been verified
    against throughout: compute the numerical gradient at x, compare
    it to the provided analytical_grad via relative_error, and return
    whether they agree within `tolerance`.

    True means "trust this analytical gradient." False means "there's
    a real bug in this backward formula, go find it before trusting
    anything built on top of it."
    """
    pass
