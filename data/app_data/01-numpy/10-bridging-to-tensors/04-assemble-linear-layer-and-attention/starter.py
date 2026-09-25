import numpy as np


def init_linear_params(
    rng: np.random.Generator, in_features: int, out_features: int, device: str = "cpu"
) -> dict:
    """
    Create the parameters of a linear layer as tensor records
    (dictionaries with "data", "device", "requires_grad").

    Return {"W": <record>, "b": <record>} where:
      W data: He-initialized weights of shape (in_features, out_features),
              drawn from rng.normal(0.0, np.sqrt(2.0 / in_features),
              (in_features, out_features)), then cast to float32
      b data: zeros of shape (out_features,), dtype float32
      both records: the given `device`, requires_grad=True
    """
    pass


def linear_forward(x: dict, params: dict) -> dict:
    """
    Compute a linear layer on tensor record `x` (data shape
    (batch, in_features)) with params {"W": record, "b": record}.

    Raise ValueError if any two of x, W, b are on different devices,
    or if x's last dimension does not equal W's first dimension.

    Return a NEW record:
      "data":          x_data @ W_data + b_data   (bias broadcast over rows)
      "device":        the shared device
      "requires_grad": True if x, W, or b requires grad, else False
    No input may be modified.
    """
    pass


def attention_weights(q: np.ndarray, k: np.ndarray) -> np.ndarray:
    """
    `q` has shape (n_q, d) and `k` has shape (n_k, d).
    Return an array of shape (n_q, n_k): the row-wise softmax of
    (q @ k.T) / sqrt(d), computed with the max-subtraction trick for
    numerical stability (subtract each row's maximum before applying
    np.exp). Use axis-based aggregation and np.newaxis; no Python loops.

    Raise ValueError if q and k have different last dimensions.
    Inputs must not be modified.
    """
    pass
