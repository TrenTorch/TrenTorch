import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def prefix_tuning_augment(key: np.ndarray, value: np.ndarray, prefix_keys: np.ndarray, prefix_values: np.ndarray):
    """
    Prefix tuning (Li & Liang, 2021): prepend a set of LEARNABLE
    key/value vectors to every attention layer's real keys/values.
    The base model's weights stay completely frozen -- only these
    prefix vectors (one learnable K/V pair set per layer) get trained,
    letting them act like a "steering" context every query attends to.
    """
    # TODO: np.concatenate([prefix_keys, key], axis=0) and the same for
    # value/prefix_values, keeping the prefix FIRST in sequence order.
    pass


def prompt_tuning_augment(input_embeddings: np.ndarray, soft_prompt_embeddings: np.ndarray) -> np.ndarray:
    """
    Prompt tuning (Lester et al., 2021): an even lighter-weight cousin
    of prefix tuning -- instead of learnable K/V pairs at EVERY layer,
    prepend learnable "soft" (virtual, non-discrete) token embeddings
    ONLY at the very input, before the first layer even runs. The rest
    of the network processes them exactly like any other token
    embedding.
    """
    # TODO: np.concatenate([soft_prompt_embeddings, input_embeddings], axis=0)
    pass


def count_trainable_parameters_prefix_tuning(num_layers: int, prefix_len: int, hidden_dim: int) -> int:
    """
    Prefix tuning trains a fresh K/V prefix pair PER LAYER: 2 (K and V)
    * prefix_len * hidden_dim parameters, for each of num_layers.
    """
    # TODO: num_layers * prefix_len * hidden_dim * 2
    pass


def count_trainable_parameters_prompt_tuning(prompt_len: int, hidden_dim: int) -> int:
    """
    Prompt tuning trains ONLY the input-layer soft embeddings --
    prompt_len * hidden_dim parameters total, regardless of how many
    layers the model has.
    """
    # TODO: prompt_len * hidden_dim
    pass
