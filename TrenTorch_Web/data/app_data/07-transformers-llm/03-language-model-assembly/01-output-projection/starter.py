import numpy as np


def output_projection(hidden_states: np.ndarray, output_weight: np.ndarray) -> np.ndarray:
    """
    Projects the final Transformer block's `d_model`-sized hidden states
    to `vocab_size`-sized logits, one score per vocabulary word, ready to
    be turned into next-token probabilities by softmax.
    """
    pass
