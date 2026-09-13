import random

import numpy as np


def seeded_numpy_sequence(seed: int, n: int) -> np.ndarray:
    """
    A sequence of n random numbers from a NumPy generator seeded with
    `seed`. The whole point of a seed: this must produce the EXACT
    same sequence every single time it's called with the same seed.
    """
    # TODO: rng = np.random.default_rng(seed). Return rng.random(n).
    pass


def seeded_python_random_sequence(seed: int, n: int) -> list:
    """
    The SAME idea, but using Python's OWN built-in `random` module --
    a genuinely SEPARATE source of randomness from NumPy's generator,
    with its own independent seed.
    """
    # TODO: rng = random.Random(seed). Return [rng.random() for _ in
    # range(n)].
    pass


def capture_reproducibility_config(numpy_seed: int, python_seed: int) -> dict:
    """
    A real training run has MULTIPLE independent sources of
    randomness that all need pinning separately -- this bundles both
    seeds together into one config, the kind of thing you'd actually
    log alongside a run (01-experiment-tracking's log_metric/
    log_artifact) so the run can be reproduced later.
    """
    # TODO: return {"numpy_seed": numpy_seed, "python_random_seed": python_seed}
    pass


def verify_reproducible(fn, seed: int, num_trials: int = 3) -> bool:
    """
    Calls `fn(seed)` several times and confirms every call produces
    the EXACT same result -- the actual, practical test of whether a
    training run's randomness has genuinely been pinned, rather than
    just assuming a seed was set correctly somewhere.
    """
    # TODO: call fn(seed) num_trials times, collecting results. Return
    # True only if every result equals the first one (np.array_equal
    # works for both arrays and plain lists).
    pass
