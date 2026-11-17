
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear


def column_parallel_linear(input: np.ndarray, weight_shards: list, bias_shards: list) -> np.ndarray:
    outputs = [linear(input, w, b) for w, b in zip(weight_shards, bias_shards)]
    return np.concatenate(outputs, axis=-1)


def row_parallel_linear(input_shards: list, weight_shards: list, bias: np.ndarray) -> np.ndarray:
    partials = [linear(x, w) for x, w in zip(input_shards, weight_shards)]
    return sum(partials) + bias


def split_weight_by_output_features(weight: np.ndarray, bias: np.ndarray, num_gpus: int):
    return list(np.array_split(weight, num_gpus, axis=0)), list(np.array_split(bias, num_gpus, axis=0))


def split_by_input_features(input: np.ndarray, weight: np.ndarray, num_gpus: int):
    return list(np.array_split(input, num_gpus, axis=-1)), list(np.array_split(weight, num_gpus, axis=1))
