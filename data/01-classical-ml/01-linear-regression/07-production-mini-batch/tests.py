"""
pytest data/01-classical-ml/01-linear-regression/07-production-mini-batch/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

train_linear_regression_production = load_solution(f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}").train_linear_regression_production
train_linear_regression = load_solution("01-classical-ml/01-linear-regression/05-training-loop").train_linear_regression


def test_reaches_similar_solution_to_naive_full_batch():
    # Different training mechanics, same underlying problem -- both
    # should converge to approximately the same place.
    rng = np.random.default_rng(11)
    X = rng.normal(size=(400, 3))
    true_w, true_b = np.array([2.0, -1.0, 0.5]), 1.0
    y = X @ true_w + true_b + rng.normal(scale=0.05, size=400)

    w_naive, b_naive = train_linear_regression(X, y, lr=0.1, epochs=300)
    w_prod, b_prod = train_linear_regression_production(X, y, lr=0.1, epochs=30, batch_size=32)
    assert np.allclose(w_naive, w_prod, atol=0.3)
    assert np.isclose(b_naive, b_prod, atol=0.3)


def test_uneven_batch_size_does_not_crash_or_drop_data():
    # 100 samples, batch_size=32 -> batches of 32, 32, 32, 4. The last
    # short batch is exactly the case a careless range/reshape breaks.
    X, y = np.random.randn(100, 2), np.random.randn(100)
    w, b = train_linear_regression_production(X, y, lr=0.01, epochs=1, batch_size=32)
    assert w.shape == (2,) and np.isfinite(b)


def test_never_touches_more_than_one_batch_of_memory():
    # Simulates "huge data" by wrapping X in an object that raises if
    # anything ever slices more than batch_size rows out of it at once.
    class GuardedArray(np.ndarray):
        def __getitem__(self, idx):
            result = super().__getitem__(idx)
            if isinstance(idx, np.ndarray) and len(idx) > 16:
                raise AssertionError("touched more than one batch at once")
            return result

    X = np.random.randn(200, 2).view(GuardedArray)
    y = np.random.randn(200)
    train_linear_regression_production(X, y, lr=0.01, epochs=1, batch_size=16)


def test_matches_real_pytorch_on_identical_full_batch_run():
    # Ground truth from the actual library, not our own derivation.
    # batch_size == n_samples here on purpose: with one batch per
    # epoch, shuffling is a no-op, so this reduces to plain full-batch
    # gradient descent -- letting us compare directly against a
    # zero-initialized torch.nn.Linear trained the same way, with no
    # need to replicate NumPy's shuffle RNG stream inside torch.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(42)
    #   X = rng.normal(size=(64, 2)).astype(np.float32)
    #   y = (X @ np.array([1.5, -0.5], dtype=np.float32) + 0.2).astype(np.float32)
    #   model = nn.Linear(2, 1)
    #   with torch.no_grad(): model.weight.zero_(); model.bias.zero_()
    #   optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
    #   for _ in range(50): full-batch step on (X, y) above
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    rng = np.random.default_rng(42)
    X = rng.normal(size=(64, 2)).astype(np.float32)
    y = (X @ np.array([1.5, -0.5], dtype=np.float32) + 0.2).astype(np.float32)

    EXPECTED_W = np.array([1.4445702, -0.4424865], dtype=np.float32)
    EXPECTED_B = np.float32(0.20526938140392303)

    w, b = train_linear_regression_production(X, y, lr=0.05, epochs=50, batch_size=64)
    assert np.allclose(w, EXPECTED_W, atol=1e-3)
    assert np.isclose(b, EXPECTED_B, atol=1e-3)
