import numpy as np


def rnn_cell_backward(
    grad_h: np.ndarray,
    h_next: np.ndarray,
    x: np.ndarray,
    h_prev: np.ndarray,
    weight_ih: np.ndarray,
    weight_hh: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    The backward pass of `[01-rnn-cell-forward]`'s rnn_cell_forward.
    `grad_h` is the upstream gradient with respect to h_next (this
    cell's OWN output); `h_next` is that output itself (needed for the
    tanh backward rule, since tanh's derivative is expressed in terms of
    its OWN output: d/dz tanh(z) = 1 - tanh(z)^2). Returns gradients
    with respect to every one of rnn_cell_forward's inputs:
    (grad_x, grad_h_prev, grad_weight_ih, grad_weight_hh, grad_bias_ih,
    grad_bias_hh).
    """
    pass
