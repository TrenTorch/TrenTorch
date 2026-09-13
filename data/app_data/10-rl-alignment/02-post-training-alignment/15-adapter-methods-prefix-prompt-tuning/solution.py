import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def prefix_tuning_augment(key: np.ndarray, value: np.ndarray, prefix_keys: np.ndarray, prefix_values: np.ndarray):
    augmented_key = np.concatenate([prefix_keys, key], axis=0)
    augmented_value = np.concatenate([prefix_values, value], axis=0)
    return augmented_key, augmented_value


def prompt_tuning_augment(input_embeddings: np.ndarray, soft_prompt_embeddings: np.ndarray) -> np.ndarray:
    return np.concatenate([soft_prompt_embeddings, input_embeddings], axis=0)


def count_trainable_parameters_prefix_tuning(num_layers: int, prefix_len: int, hidden_dim: int) -> int:
    return num_layers * prefix_len * hidden_dim * 2


def count_trainable_parameters_prompt_tuning(prompt_len: int, hidden_dim: int) -> int:
    return prompt_len * hidden_dim
