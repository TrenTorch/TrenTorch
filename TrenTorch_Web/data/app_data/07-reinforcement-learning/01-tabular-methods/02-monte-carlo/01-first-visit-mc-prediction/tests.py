import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
estimate_state_values = _module.estimate_state_values


def test_single_episode_single_state():
    """Single episode, single state."""
    episode = [("A", 10.0)]
    values = estimate_state_values([episode], gamma=0.9)
    assert values["A"] == 10.0


def test_single_episode_multiple_states():
    """Single episode: (A, 10) -> (B, 5) -> (C, 2)."""
    episode = [("A", 10.0), ("B", 5.0), ("C", 2.0)]
    values = estimate_state_values([episode], gamma=0.9)

    # A: 10 + 0.9*5 + 0.81*2 = 10 + 4.5 + 1.62 = 16.12
    assert np.isclose(values["A"], 16.12)
    # B: 5 + 0.9*2 = 6.8
    assert np.isclose(values["B"], 6.8)
    # C: 2
    assert np.isclose(values["C"], 2.0)


def test_multiple_episodes_averaging():
    """Multiple episodes: average returns from first visits."""
    ep1 = [("A", 10.0), ("B", 5.0)]
    ep2 = [("A", 20.0), ("B", 3.0)]
    episodes = [ep1, ep2]

    values = estimate_state_values(episodes, gamma=1.0)
    # A: avg(15, 20) = 17.5
    assert np.isclose(values["A"], 17.5)
    # B: avg(5, 3) = 4
    assert np.isclose(values["B"], 4.0)


def test_first_visit_semantics():
    """First-visit: state appears twice, only first visit counts."""
    episode = [("A", 10.0), ("B", 5.0), ("A", 3.0), ("C", 1.0)]
    values = estimate_state_values([episode], gamma=0.9)

    # A first visit at index 0: 10 + 0.9*5 + 0.81*3 + 0.729*1
    expected_A = 10.0 + 0.9*5.0 + 0.81*3.0 + 0.729*1.0
    assert np.isclose(values["A"], expected_A)


def test_empty_episodes():
    """Empty episode list."""
    values = estimate_state_values([], gamma=0.9)
    assert values == {}


def test_zero_gamma():
    """gamma=0: only immediate reward counts."""
    episode = [("A", 10.0), ("B", 100.0)]
    values = estimate_state_values([episode], gamma=0.0)
    assert np.isclose(values["A"], 10.0)
    assert np.isclose(values["B"], 100.0)


def test_gamma_one():
    """gamma=1: all rewards count equally."""
    episode = [("A", 1.0), ("B", 2.0), ("C", 3.0)]
    values = estimate_state_values([episode], gamma=1.0)
    assert np.isclose(values["A"], 6.0)
    assert np.isclose(values["B"], 5.0)
    assert np.isclose(values["C"], 3.0)


def test_many_episodes():
    """Multiple episodes with averaging."""
    episodes = [
        [("A", 5.0)],
        [("A", 10.0)],
        [("A", 15.0)]
    ]
    values = estimate_state_values(episodes, gamma=1.0)
    assert np.isclose(values["A"], 10.0)


def test_partial_state_coverage():
    """Some states appear in some episodes, not others."""
    ep1 = [("A", 10.0), ("B", 5.0)]
    ep2 = [("B", 3.0), ("C", 7.0)]
    ep3 = [("A", 8.0), ("C", 9.0)]

    values = estimate_state_values([ep1, ep2, ep3], gamma=1.0)

    assert np.isclose(values["A"], (10+8)/2)  # 9
    assert np.isclose(values["B"], (5+3)/2)   # 4
    assert np.isclose(values["C"], (7+9)/2)   # 8


def test_negative_rewards():
    """Handle negative rewards."""
    episode = [("A", -10.0), ("B", 5.0)]
    values = estimate_state_values([episode], gamma=0.9)

    expected_A = -10.0 + 0.9*5.0
    assert np.isclose(values["A"], expected_A)


def test_returns_dict_independence():
    """Different states don't interfere."""
    episodes = [
        [("X", 100.0), ("Y", 1.0)],
        [("X", 200.0), ("Y", 2.0)]
    ]
    values = estimate_state_values(episodes, gamma=1.0)

    assert np.isclose(values["X"], 150.0)
    assert np.isclose(values["Y"], 1.5)
    assert "Z" not in values
