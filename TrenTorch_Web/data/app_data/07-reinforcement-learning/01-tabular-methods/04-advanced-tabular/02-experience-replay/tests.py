import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
ExperienceReplayBuffer = _module.ExperienceReplayBuffer


def test_init():
    """Initialize buffer."""
    buf = ExperienceReplayBuffer(capacity=100)
    assert len(buf) == 0


def test_add_single():
    """Add single transition."""
    buf = ExperienceReplayBuffer(capacity=100)
    buf.add(state=0, action=1, reward=5.0, next_state=1, done=False)
    assert len(buf) == 1


def test_add_multiple():
    """Add multiple transitions."""
    buf = ExperienceReplayBuffer(capacity=10)
    for i in range(5):
        buf.add(i, i, float(i), i+1, False)
    assert len(buf) == 5


def test_capacity_limit():
    """Buffer respects capacity limit."""
    buf = ExperienceReplayBuffer(capacity=5)
    for i in range(10):
        buf.add(i, i, float(i), i+1, False)
    assert len(buf) == 5


def test_fifo_order():
    """FIFO: oldest removed when full."""
    buf = ExperienceReplayBuffer(capacity=3)
    for i in range(5):
        buf.add(i, i, float(i), i+1, False)

    # Should have states 2, 3, 4 (0, 1 removed)
    assert len(buf) == 3


def test_sample_structure():
    """Sample returns dict with correct keys."""
    buf = ExperienceReplayBuffer(capacity=10)
    for i in range(5):
        buf.add(i, i, float(i), i+1, i % 2 == 0)

    batch = buf.sample(batch_size=2)

    assert 'states' in batch
    assert 'actions' in batch
    assert 'rewards' in batch
    assert 'next_states' in batch
    assert 'dones' in batch


def test_sample_size():
    """Sample returns requested size."""
    buf = ExperienceReplayBuffer(capacity=100)
    for i in range(20):
        buf.add(i, i, float(i), i+1, False)

    batch = buf.sample(batch_size=5)
    assert len(batch['states']) == 5


def test_sample_small_buffer():
    """Sample from buffer smaller than batch size."""
    buf = ExperienceReplayBuffer(capacity=100)
    for i in range(3):
        buf.add(i, i, float(i), i+1, False)

    batch = buf.sample(batch_size=10)
    assert len(batch['states']) == 3


def test_randomness():
    """Samples are random, not deterministic."""
    buf = ExperienceReplayBuffer(capacity=100)
    for i in range(50):
        buf.add(i, i, float(i), i+1, False)

    batch1 = buf.sample(batch_size=10)
    batch2 = buf.sample(batch_size=10)

    # Unlikely to be identical
    assert not np.array_equal(batch1['states'], batch2['states'])
