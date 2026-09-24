import numpy as np


def zero_out_via_view(arr: np.ndarray, start: int, stop: int) -> None:
    """
    Mutate `arr` in place so that positions [start:stop) become
    0, by obtaining a view of that range and assigning into the
    view using slice-assignment syntax (view[:] = 0). Do not
    reassign `arr` itself, and do not use boolean masking or
    fancy indexing (which would copy).
    """
    pass


def chained_view_mutation(arr: np.ndarray) -> dict:
    """
    Given a 1D array `arr` with at least 8 elements:
      1. Create view1 = arr[1:7]
      2. Create view2 = view1[2:5]  (a view of view1)
      3. Mutate view2 by setting all of its elements to -1
         (view2[:] = -1)

    Return a dictionary:
      {
        "arr": arr,          # after the mutation
        "view1": view1,       # after the mutation
        "view2": view2         # after the mutation
      }
    All three should reflect the mutation at the overlapping
    positions.
    """
    pass
