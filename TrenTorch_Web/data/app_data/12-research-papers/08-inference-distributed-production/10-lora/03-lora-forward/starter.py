import numpy as np


def lora_forward(x, W, A, B, scale):
    """
    x: inputs, shape (n, d_in)
    W: frozen pretrained weight, shape (d_out, d_in)
    A: LoRA down-projection, shape (r, d_in)
    B: LoRA up-projection, shape (d_out, r)
    scale: alpha / r

    Returns:
        The adapted layer output x W^T + scale * (x A^T) B^T, shape (n, d_out).
    """
    # TODO: Apply the frozen weight and add the scaled low-rank path (see Theory).
    pass
