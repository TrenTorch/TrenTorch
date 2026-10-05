import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
estimate_state_values_every_visit = _module.estimate_state_values_every_visit


def test_single_visit():
    """Single episode, single state."""
    episode = [("A", 10.0)]
    values = estimate_state_values_every_visit([episode], gamma=0.9)
    assert values["A"] == 10.0


def test_repeated_state():
    """State A appears twice: (A, 10) -> (B, 5) -> (A, 3)."""
    episode = [("A", 10.0), ("B", 5.0), ("A", 3.0)]
    values = estimate_state_values_every_visit([episode], gamma=0.9)

    # First A at 0: 10 + 0.9*5 + 0.81*3 = 16.12
    # Second A at 2: 3
    # Average: (16.12 + 3) / 2 = 9.56
    expected_A = (10.0 + 0.9*5.0 + 0.81*3.0 + 3.0) / 2
    assert np.isclose(values["A"], expected_A)


def test_all_same_state():
    """Episode is same state repeated."""
    episode = [("A", 1.0), ("A", 2.0), ("A", 3.0)]
    values = estimate_state_values_every_visit([episode], gamma=1.0)

    # Visit 1: 1 + 2 + 3 = 6
    # Visit 2: 2 + 3 = 5
    # Visit 3: 3
    # Average: (6 + 5 + 3) / 3 = 4.666...
    expected = (6.0 + 5.0 + 3.0) / 3
    assert np.isclose(values["A"], expected)


def test_multiple_episodes():
    """Multiple episodes with repeated states."""
    ep1 = [("A", 10.0), ("A", 5.0)]
    ep2 = [("A", 20.0)]
    episodes = [ep1, ep2]

    # ep1 visit 1: 10 + 1.0*5 = 15
    # ep1 visit 2: 5
    # ep2 visit 1: 20
    # Average: (15 + 5 + 20) / 3 = 13.333...
    values = estimate_state_values_every_visit(episodes, gamma=1.0)
    expected = (15.0 + 5.0 + 20.0) / 3
    assert np.isclose(values["A"], expected)


def test_zero_gamma():
    """gamma=0: only immediate reward counts."""
    episode = [("A", 10.0), ("B", 5.0), ("A", 8.0)]
    values = estimate_state_values_every_visit([episode], gamma=0.0)

    # First A: 10
    # Second A: 8
    # Average: 9
    assert np.isclose(values["A"], 9.0)
    assert np.isclose(values["B"], 5.0)


def test_gamma_one():
    """gamma=1: all future rewards count equally."""
    episode = [("S", 1.0), ("S", 2.0), ("S", 3.0)]
    values = estimate_state_values_every_visit([episode], gamma=1.0)

    # Visit 1: 1 + 2 + 3 = 6
    # Visit 2: 2 + 3 = 5
    # Visit 3: 3
    # Average: 14/3
    expected = 14.0 / 3.0
    assert np.isclose(values["S"], expected)


def test_different_states_independent():
    """Different states don't interfere."""
    episode = [("A", 100.0), ("B", 50.0), ("A", 25.0)]
    values = estimate_state_values_every_visit([episode], gamma=1.0)

    # A: (100 + 50 + 25 + 25) / 2 = 100
    # B: 50 + 25 = 75
    assert np.isclose(values["A"], 100.0)
    assert np.isclose(values["B"], 75.0)


def test_empty_episodes():
    """Empty episodes."""
    values = estimate_state_values_every_visit([], gamma=0.9)
    assert values == {}


def test_vs_first_visit():
    """Every-visit gives different result than first-visit when state repeats."""
    episode = [("A", 10.0), ("B", 5.0), ("A", 2.0)]

    # First-visit counts A only once: 10 + 0.9*5 + 0.81*2 = 15.62
    # Every-visit counts both: (15.62 + 2) / 2 = 8.81
    values = estimate_state_values_every_visit([episode], gamma=0.9)

    expected = (10.0 + 0.9*5.0 + 0.81*2.0 + 2.0) / 2
    assert np.isclose(values["A"], expected)


def test_long_episode():
    """Longer episode with multiple repeats."""
    episode = [("X", 1.0), ("Y", 2.0), ("X", 3.0), ("Y", 4.0), ("X", 5.0)]
    values = estimate_state_values_every_visit([episode], gamma=1.0)

    # X visits: (1+2+3+4+5) + (3+4+5) + (5) = 15 + 12 + 5 = 32
    # X count: 3, average: 32/3
    # Y visits: (2+3+4+5) + (4+5) = 14 + 9 = 23
    # Y count: 2, average: 23/2
    assert np.isclose(values["X"], 32.0 / 3.0)
    assert np.isclose(values["Y"], 23.0 / 2.0)


def test_negative_rewards():
    """Handle negative rewards."""
    episode = [("A", -10.0), ("A", 5.0)]
    values = estimate_state_values_every_visit([episode], gamma=0.9)

    # First A: -10 + 0.9*5 = -5.5
    # Second A: 5
    # Average: (-5.5 + 5) / 2 = -0.25
    expected = (-10.0 + 0.9*5.0 + 5.0) / 2
    assert np.isclose(values["A"], expected)
