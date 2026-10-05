
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear


def patch_embedding(patches: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    patches: shape (num_patches, C*patch_size*patch_size) -- flattened
        patches from 01-patchify
    weight: shape (d_model, C*patch_size*patch_size)
    bias: shape (d_model,)

    Every flattened patch is just a vector -- turning it into a
    transformer-ready "token embedding" is literally the exact same
    Linear layer this curriculum's very first question (linear
    regression's hypothesis function) already implemented. There is
    nothing patch-specific about this step at all.
    """
    # TODO: this is one line -- call the reused `linear` function on
    # `patches` with `weight` and `bias`.
    pass
