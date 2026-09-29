import numpy as np


def save_checkpoint(params: dict[str, np.ndarray], epoch: int, path: str) -> None:
    np.savez(path, __epoch__=np.array(epoch), **params)


def load_checkpoint(path: str) -> tuple[dict[str, np.ndarray], int]:
    with np.load(path) as data:
        epoch = int(data["__epoch__"])
        params = {key: data[key] for key in data.files if key != "__epoch__"}
    return params, epoch
