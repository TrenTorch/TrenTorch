import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


def column_parallel_linear(input: np.ndarray, weight_shards: list, bias_shards: list) -> np.ndarray:
    """
    Megatron-LM-style COLUMN-parallel linear layer: each GPU holds a
    slice of the OUTPUT features (a row-slice of the full weight
    matrix, `linear`'s (out_features, in_features) convention), so
    every GPU can compute its slice of the output independently from
    the SAME full input -- no communication needed until the very end,
    where the slices are concatenated back into the full output.
    """
    # TODO: for each (w, b) in zip(weight_shards, bias_shards), compute
    # linear(input, w, b), then np.concatenate the results along the
    # last axis.
    pass


def row_parallel_linear(input_shards: list, weight_shards: list, bias: np.ndarray) -> np.ndarray:
    """
    Megatron-LM-style ROW-parallel linear layer: each GPU holds a
    slice of the INPUT features (a column-slice of the full weight
    matrix) and the matching slice of the input -- each GPU computes a
    PARTIAL output using only its slice, and an all-reduce (here: a
    plain sum) combines the partials into the true full output before
    the (un-split) bias is added once.
    """
    # TODO: for each (x, w) in zip(input_shards, weight_shards), compute
    # linear(x, w) (no bias yet), sum all the partials, then add bias.
    pass


def split_weight_by_output_features(weight: np.ndarray, bias: np.ndarray, num_gpus: int):
    """
    Splits a (out_features, in_features) weight and its bias into
    num_gpus row-slices -- the setup column_parallel_linear expects.
    """
    # TODO: np.array_split weight along axis 0 and bias along axis 0.
    pass


def split_by_input_features(input: np.ndarray, weight: np.ndarray, num_gpus: int):
    """
    Splits an input's last (feature) axis and a weight's in_features
    axis (axis 1) into matching num_gpus column-slices -- the setup
    row_parallel_linear expects.
    """
    # TODO: np.array_split input along axis -1 and weight along axis 1.
    pass
