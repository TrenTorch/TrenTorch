
import numpy as np

from _load import load_solution

gradient = load_solution("math-partial-derivatives").gradient


def directional_derivative(f, x: np.ndarray, direction: np.ndarray, eps: float = 1e-5) -> float:
    """
    How fast f changes as x moves along `direction` (not necessarily
    one of the coordinate axes 02-partial-derivatives restricted to).

    Normalize `direction` to a unit vector first (its actual length
    shouldn't change the answer, only which way it points), then apply
    01-derivatives-first-principles' central difference formula along
    that unit vector instead of a single coordinate.
    """
    pass


def steepest_ascent_direction(f, x: np.ndarray) -> np.ndarray:
    """
    Returns the unit vector pointing in the direction f increases
    fastest at x. `gradient` is already provided above.
    """
    pass
