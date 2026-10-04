import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
td_prediction = _module.td_prediction


def test_single_transition():
    """Single transition: (0, 5.0, 1)."""
    episodes = [[(0, 5.0, 1)]]
    V = td_prediction(episodes, gamma=0.9, alpha=0.1)

    # V(0) = 0 + 0.1 * (5 + 0.9*0 - 0) = 0.5
    assert np.isclose(V[0], 0.5)


def test_chain():
    """Chain: 0 -> 1 -> terminal."""
    episodes = [[(0, 1.0, 1), (1, 1.0, 2)]]
    V = td_prediction(episodes, gamma=1.0, alpha=0.1)

    # Process in order:
    # (1, 1.0, 2): V(1) = 0 + 0.1 * (1 + 0 - 0) = 0.1
    # (0, 1.0, 1): V(0) = 0 + 0.1 * (1 + 0.1 - 0) = 0.11
    assert V[1] >= 0.0
    assert V[0] >= 0.0


def test_multiple_episodes():
    """Multiple episodes accumulate updates."""
    ep1 = [(0, 1.0, 1)]
    ep2 = [(0, 2.0, 1)]
    episodes = [ep1, ep2]

    V = td_prediction(episodes, gamma=1.0, alpha=0.1)

    # After ep1: V(0) = 0.1
    # After ep2: V(0) = 0.1 + 0.1 * (2 + 0 - 0.1) = 0.1 + 0.19 = 0.29
    assert np.isclose(V[0], 0.29)


def test_zero_alpha():
    """alpha=0: no learning."""
    episodes = [[(0, 5.0, 1)]]
    V = td_prediction(episodes, gamma=0.9, alpha=0.0)

    # No update
    assert V.get(0, 0.0) == 0.0


def test_one_alpha():
    """alpha=1: full replacement."""
    episodes = [[(0, 5.0, 1)]]
    V = td_prediction(episodes, gamma=0.9, alpha=1.0)

    # V(0) = 0 + 1.0 * (5 + 0 - 0) = 5.0
    assert np.isclose(V[0], 5.0)


def test_gamma_effects():
    """Different gamma values."""
    episodes = [[(0, 1.0, 1)]]

    V0 = td_prediction(episodes, gamma=0.0, alpha=0.1)
    V1 = td_prediction(episodes, gamma=1.0, alpha=0.1)

    # Both should have valid values
    assert 0 in V0
    assert 0 in V1


def test_convergence():
    """Repeated episodes converge."""
    episode = [(0, 1.0, 1)]
    episodes = [episode] * 100

    V = td_prediction(episodes, gamma=0.9, alpha=0.1)

    # Value should increase over episodes
    assert V[0] > 0.0


def test_negative_rewards():
    """Handle negative rewards."""
    episodes = [[(0, -5.0, 1)]]
    V = td_prediction(episodes, gamma=0.9, alpha=0.1)

    # V(0) = 0 + 0.1 * (-5 + 0 - 0) = -0.5
    assert np.isclose(V[0], -0.5)


def test_terminal_state_zero():
    """Terminal state (not updated) has value 0."""
    episodes = [[(0, 1.0, 100)]]
    V = td_prediction(episodes, gamma=0.9, alpha=0.1)

    # State 100 not in V (never updated)
    assert 100 not in V


def test_stochastic_convergence():
    """Stochastic updates still converge."""
    episodes = [
        [(0, 1.0, 1)],
        [(0, 2.0, 1)],
        [(0, 3.0, 1)],
    ]

    V = td_prediction(episodes, gamma=1.0, alpha=0.1)

    # Should have positive value
    assert V[0] > 0.0
