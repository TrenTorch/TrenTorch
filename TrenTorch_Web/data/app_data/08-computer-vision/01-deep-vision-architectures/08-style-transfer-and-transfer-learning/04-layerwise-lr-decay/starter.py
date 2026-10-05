def layer_index(name: str, n_layers: int) -> int:
    """embed -> 0, layers.i -> i + 1, head -> n_layers + 1 (ValueError otherwise)."""
    # TODO
    pass


def layerwise_lr(name: str, n_layers: int, base_lr: float, decay: float) -> float:
    """base_lr * decay ** (n_layers + 1 - layer_index)."""
    # TODO
    pass
