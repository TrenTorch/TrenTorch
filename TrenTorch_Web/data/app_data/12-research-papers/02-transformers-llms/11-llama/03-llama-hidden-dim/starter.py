def llama_hidden_dim(dim, multiple_of=256):
    """
    dim: model width d
    multiple_of: the hidden width is rounded up to a multiple of this

    Returns:
        The SwiGLU hidden width: about 8d/3, rounded up to a multiple of multiple_of.
    """
    # TODO: Compute int(8 * dim / 3), then round up to a multiple of multiple_of (see Theory).
    pass
