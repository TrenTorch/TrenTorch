import numpy as np


def try_broadcast_add(a: np.ndarray, b: np.ndarray) -> dict:
    """
    Attempt to compute a + b. Return a dictionary:
      {
        "success": <True if the addition succeeded, False if it
                     raised a ValueError>,
        "result": <the resulting array if success, else None>,
        "shape_a": a.shape,
        "shape_b": b.shape
      }
    Do not let the ValueError propagate out of this function —
    catch it and report success=False instead.
    """
    pass


def find_first_incompatible_axis(shape_a: tuple, shape_b: tuple):
    """
    Given two shapes, find the first dimension position (counted
    from the right, as 0, -1, -2, ... or however you choose to
    express position, just be consistent) where they fail to be
    broadcast-compatible according to the rule from the previous
    topic. Return None if the shapes are fully compatible.

    Return the position as a negative index counting from the
    end (e.g. -1 for the trailing dimension), matching how
    broadcasting itself aligns dimensions.
    """
    pass
