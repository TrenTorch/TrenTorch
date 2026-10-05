import numpy as np


def bptt_gradient_norms(seq_len: int, weight_hh: np.ndarray, grad_h_final: np.ndarray) -> list[float]:
    """
    A simplified model of backpropagation through time: starting from
    the gradient at the LAST time step (`grad_h_final`), repeatedly
    multiplies it by the SAME recurrent weight matrix `weight_hh`,
    `seq_len` times, walking the gradient backward through the sequence
    one step at a time (mirroring `[02-rnn-cell-backward]`'s
    `grad_h_prev = grad_z @ weight_hh`, with the tanh-derivative term
    simplified away to isolate weight_hh's own compounding effect).
    Returns the gradient's norm after each step, length seq_len + 1
    (the starting norm, followed by one entry per step).
    """
    pass
