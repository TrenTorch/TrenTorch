import numpy as np


def sinusoidal_positional_encoding(seq_len: int, d_model: int) -> np.ndarray:
    """
    Builds the fixed (non-learned) sinusoidal positional encoding table
    from "Attention Is All You Need", shape (seq_len, d_model): one row
    per position, giving every position a unique, smoothly-varying
    pattern the model can use to tell WHERE in the sequence a token sits.

        PE(pos, 2i)   = sin(pos / 10000^(2i / d_model))
        PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))
    """
    position = np.arange(seq_len)[:, None]
    div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))
    pass
