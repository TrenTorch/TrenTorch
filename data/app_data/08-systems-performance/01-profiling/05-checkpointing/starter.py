import numpy as np


def save_checkpoint(params: dict[str, np.ndarray], epoch: int, path: str) -> None:
    """
    params: a dict mapping parameter names to arrays (e.g.
        {"layer1.weight": ..., "layer1.bias": ...})
    epoch: which training epoch this checkpoint was taken at
    path: file path to write to, expected to already end in ".npz"

    Save every named parameter array AND the epoch number to a single
    file on disk, so training can be resumed later exactly where it
    left off.
    """
    # TODO: np.savez(path, ...) can take keyword arguments, one per
    # array to save, plus dict-unpacking (**params) to pass every
    # parameter through by name. Save the epoch under some key that
    # can't collide with a real parameter name (e.g. "__epoch__").
    pass


def load_checkpoint(path: str) -> tuple[dict[str, np.ndarray], int]:
    """
    path: the exact same path save_checkpoint was called with

    Returns (params, epoch): params is a dict with the same
    name -> array mapping that was saved, epoch is the plain int that
    was saved alongside them.
    """
    # TODO: np.load(path) returns an NpzFile object; iterate its
    # `.files` attribute (the list of saved array names) to rebuild the
    # params dict, skipping whichever key you used for the epoch, and
    # convert that key's value back to a plain int with int(...).
    pass
