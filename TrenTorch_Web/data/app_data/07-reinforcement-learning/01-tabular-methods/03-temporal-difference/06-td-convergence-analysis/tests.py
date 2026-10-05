import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
td_convergence_analysis = _module.td_convergence_analysis


def test_single_episode():
    """Single episode analysis."""
    episodes = [[(0, 1.0, 1)]]
    true_values = {0: 1.0, 1: 0.0}

    V, mse = td_convergence_analysis(episodes, true_values, gamma=0.9, alpha=0.1)

    assert len(mse) == 1
    assert mse[0] >= 0.0


def test_convergence_decreases():
    """MSE should generally decrease."""
    # Create a simple chain environment
    episodes = [
        [(0, 1.0, 1)],
        [(0, 1.0, 1)],
        [(0, 1.0, 1)],
        [(0, 1.0, 1)],
        [(0, 1.0, 1)],
    ]
    true_values = {0: 1.0, 1: 0.0}

    V, mse = td_convergence_analysis(episodes, true_values, gamma=1.0, alpha=0.1)

    # Last MSE should be smaller than first
    assert mse[-1] <= mse[0]


def test_mse_structure():
    """MSE list has correct structure."""
    episodes = [[(0, 1.0, 1)], [(0, 2.0, 1)]]
    true_values = {0: 1.5, 1: 0.0}

    V, mse = td_convergence_analysis(episodes, true_values, gamma=0.9, alpha=0.1)

    assert isinstance(mse, list)
    assert len(mse) == 2
    assert all(isinstance(x, (float, np.floating)) for x in mse)


def test_v_estimates_structure():
    """V estimates dict structure."""
    episodes = [[(0, 1.0, 1), (1, 0.5, 2)]]
    true_values = {0: 1.0, 1: 0.5, 2: 0.0}

    V, _ = td_convergence_analysis(episodes, true_values, gamma=0.9, alpha=0.1)

    assert isinstance(V, dict)
    assert 0 in V
    assert 1 in V


def test_zero_alpha():
    """alpha=0: no learning."""
    episodes = [[(0, 10.0, 1)], [(0, 10.0, 1)]]
    true_values = {0: 10.0, 1: 0.0}

    V, mse = td_convergence_analysis(episodes, true_values, gamma=0.9, alpha=0.0)

    # V(0) should remain 0
    assert np.isclose(V.get(0, 0.0), 0.0)


def test_one_alpha():
    """alpha=1: full update."""
    episodes = [[(0, 5.0, 1)]]
    true_values = {0: 5.0, 1: 0.0}

    V, _ = td_convergence_analysis(episodes, true_values, gamma=0.9, alpha=1.0)

    # V(0) = 0 + 1.0 * (5 + 0 - 0) = 5.0
    assert np.isclose(V[0], 5.0)


def test_multiple_states():
    """Analysis with multiple states."""
    episodes = [
        [(0, 1.0, 1), (1, 2.0, 2)],
        [(0, 1.0, 1), (1, 2.0, 2)],
    ]
    true_values = {0: 1.0, 1: 2.0, 2: 0.0}

    V, mse = td_convergence_analysis(episodes, true_values, gamma=1.0, alpha=0.1)

    assert len(mse) == 2
    assert all(m >= 0.0 for m in mse)


def test_deterministic():
    """Same input gives same output."""
    episodes = [[(0, 1.0, 1)], [(0, 1.5, 1)]]
    true_values = {0: 1.25, 1: 0.0}

    V1, mse1 = td_convergence_analysis(episodes, true_values, gamma=0.9, alpha=0.1)
    V2, mse2 = td_convergence_analysis(episodes, true_values, gamma=0.9, alpha=0.1)

    assert np.allclose(mse1, mse2)
