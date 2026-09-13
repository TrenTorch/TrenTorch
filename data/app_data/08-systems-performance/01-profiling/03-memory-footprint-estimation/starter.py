import numpy as np

_BYTES_PER_DTYPE = {
    "float32": 4,
    "float16": 2,
    "bfloat16": 2,
    "int8": 1,
}


def estimate_memory_bytes(params: list[np.ndarray], dtype: str = "float32") -> int:
    """
    params: a list of parameter arrays (shapes only matter, not the
        actual stored dtype -- this estimates what storing them AS
        `dtype` would cost)
    dtype: one of "float32", "float16", "bfloat16", "int8"

    Returns the total number of bytes it would take to store every
    parameter at the given dtype's bit width.
    """
    # TODO: total element count (reuse the same idea as
    # 02-parameter-counting) times _BYTES_PER_DTYPE[dtype].
    pass


def estimate_optimizer_memory_bytes(
    params: list[np.ndarray], dtype: str = "float32", optimizer: str = "sgd"
) -> int:
    """
    Returns the TOTAL memory a training step needs: the parameters
    themselves, PLUS their gradients (always the same size as the
    parameters), PLUS whatever extra per-parameter state the optimizer
    keeps:
      "sgd"      -> no extra state
      "momentum" -> one extra copy per parameter (the momentum buffer)
      "adam"     -> two extra copies per parameter (first and second
                    moment estimates)
    """
    # TODO: param_bytes = estimate_memory_bytes(params, dtype).
    # gradient_bytes is the same as param_bytes (one gradient per
    # parameter, same shape and dtype). optimizer_state_bytes is
    # param_bytes times 0/1/2 depending on `optimizer`. Return the sum
    # of all three.
    pass
