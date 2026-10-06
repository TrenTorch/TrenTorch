import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
prioritized_replay_buffer = _module.prioritized_replay_buffer


def test_basic_sampling():
    """Basic PER sampling."""
    transitions = [(i, i, i, i, False) for i in range(10)]
    td_errors = [1.0, 2.0, 0.1, 0.5, 1.5, 0.2, 3.0, 1.0, 0.3, 2.5]

    indices = prioritized_replay_buffer(transitions, td_errors, batch_size=5, alpha=0.6)

    assert len(indices) == 5
    assert all(0 <= i < 10 for i in indices)


def test_deterministic_with_seed():
    """Determinism with seed."""
    np.random.seed(42)
    transitions = list(range(10))
    td_errors = [1.0] * 10

    np.random.seed(42)
    indices1 = prioritized_replay_buffer(transitions, td_errors, batch_size=5, alpha=0.6)

    np.random.seed(42)
    indices2 = prioritized_replay_buffer(transitions, td_errors, batch_size=5, alpha=0.6)

    assert np.array_equal(indices1, indices2)


def test_high_error_oversampled():
    """High TD-error transitions oversampled."""
    transitions = list(range(2))
    td_errors = [10.0, 0.1]  # Huge difference

    # Sample many times, see which is sampled more
    np.random.seed(0)
    all_indices = []
    for _ in range(100):
        indices = prioritized_replay_buffer(transitions, td_errors, batch_size=1, alpha=1.0)
        all_indices.extend(indices)

    count_0 = sum(1 for i in all_indices if i == 0)
    count_1 = sum(1 for i in all_indices if i == 1)

    # Index 0 should be sampled much more
    assert count_0 > count_1 * 5


def test_alpha_zero_uniform():
    """alpha=0 approximates uniform."""
    transitions = list(range(4))
    td_errors = [1.0, 100.0, 50.0, 2.0]  # Big differences

    np.random.seed(0)
    counts = [0] * 4
    for _ in range(400):
        indices = prioritized_replay_buffer(transitions, td_errors, batch_size=1, alpha=0.0)
        counts[indices[0]] += 1

    # With alpha=0, should be roughly uniform
    assert min(counts) > 50  # All sampled reasonably often


def test_batch_size():
    """Batch size respected."""
    transitions = list(range(20))
    td_errors = np.ones(20)

    for batch_size in [1, 5, 10, 20]:
        indices = prioritized_replay_buffer(transitions, td_errors, batch_size=batch_size, alpha=0.6)
        assert len(indices) == batch_size


def test_zero_errors():
    """Handle zero TD-errors with epsilon."""
    transitions = list(range(3))
    td_errors = [0.0, 0.0, 0.0]

    # Should not crash
    indices = prioritized_replay_buffer(transitions, td_errors, batch_size=2, alpha=0.6)
    assert len(indices) == 2


def test_negative_errors_abs():
    """Negative errors handled (take absolute value)."""
    transitions = list(range(2))
    td_errors = [-5.0, 1.0]  # Negative error

    indices = prioritized_replay_buffer(transitions, td_errors, batch_size=100, alpha=0.6)

    # Should prefer index 0 (higher absolute error)
    assert sum(1 for i in indices if i == 0) > sum(1 for i in indices if i == 1)
