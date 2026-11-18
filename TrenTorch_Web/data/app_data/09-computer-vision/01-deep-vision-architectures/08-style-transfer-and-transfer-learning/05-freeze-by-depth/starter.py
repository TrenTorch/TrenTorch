def trainable_mask(names: list[str], n_frozen: int) -> list[bool]:
    """False for embed and layers.i with i < n_frozen (embed frozen when n_frozen >= 1); True otherwise."""
    # TODO
    pass


def count_trainable(sizes: list[int], mask: list[bool]) -> int:
    """Number of trainable parameters."""
    # TODO
    pass


def fraction_trainable(sizes: list[int], mask: list[bool]) -> float:
    """Trainable parameters divided by all parameters."""
    # TODO
    pass
