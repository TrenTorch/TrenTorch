def transformer_params(n_layers: int, d_model: int, vocab: int, d_ff: int | None = None, tied: bool = True) -> int:
    """Parameters of a decoder-only transformer (no biases or norms)."""
    # TODO
    pass


def training_flops(n_params: float, n_tokens: float) -> float:
    """About 6 FLOPs per parameter per token."""
    # TODO
    pass


def chinchilla_tokens(n_params: float) -> float:
    """Compute-optimal token count, 20 tokens per parameter."""
    # TODO
    pass
