import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
evaluate_state_value = _module.evaluate_state_value


def test_single_trajectory_single_visit():
    """Single trajectory, state appears once."""
    # Trajectory: (A, 5) -> (B, 3) -> (C, 2)
    # If querying state A with gamma=0.9:
    # Return = 5 + 0.9*3 + 0.81*2 = 5 + 2.7 + 1.62 = 9.32
    trajectory = [("A", 5.0), ("B", 3.0), ("C", 2.0)]
    value = evaluate_state_value([trajectory], "A", 0.9)
    expected = 5.0 + 0.9 * 3.0 + 0.81 * 2.0
    assert np.isclose(value, expected)


def test_multiple_trajectories():
    """Multiple trajectories, average their values."""
    traj1 = [("A", 10.0), ("B", 5.0)]
    traj2 = [("A", 10.0), ("B", 5.0)]
    traj3 = [("A", 10.0), ("B", 5.0)]
    gamma = 1.0  # No discounting for simplicity
    value = evaluate_state_value([traj1, traj2, traj3], "A", gamma)
    expected = (15.0 + 15.0 + 15.0) / 3.0
    assert np.isclose(value, expected)


def test_state_not_visited():
    """If state never appears, return 0."""
    trajectory = [("A", 5.0), ("B", 3.0)]
    value = evaluate_state_value([trajectory], "C", 0.9)
    assert value == 0.0


def test_empty_trajectories():
    """Empty trajectory list returns 0."""
    value = evaluate_state_value([], "A", 0.9)
    assert value == 0.0


def test_first_visit_semantics():
    """First-visit: if state appears twice, only first counts."""
    # Trajectory: (A, 10) -> (B, 5) -> (A, 3) -> (C, 1)
    # For state A, first visit at index 0: return = 10 + 0.9*5 + 0.81*3 + 0.729*1
    trajectory = [("A", 10.0), ("B", 5.0), ("A", 3.0), ("C", 1.0)]
    gamma = 0.9
    value = evaluate_state_value([trajectory], "A", gamma)
    expected = 10.0 + 0.9 * 5.0 + 0.81 * 3.0 + 0.729 * 1.0
    assert np.isclose(value, expected)


def test_state_at_end():
    """State can be the last state in trajectory."""
    trajectory = [("A", 10.0), ("B", 5.0), ("C", 3.0)]
    value = evaluate_state_value([trajectory], "C", 0.9)
    expected = 3.0
    assert np.isclose(value, expected)


def test_zero_discount():
    """With gamma=0, only immediate reward counts."""
    trajectory = [("A", 10.0), ("B", 5.0), ("C", 3.0)]
    value = evaluate_state_value([trajectory], "A", 0.0)
    assert np.isclose(value, 10.0)


def test_mixed_trajectories():
    """Some trajectories contain state, some don't."""
    traj1 = [("A", 10.0), ("B", 5.0)]  # Contains A
    traj2 = [("X", 1.0), ("Y", 2.0)]   # No A
    traj3 = [("A", 15.0), ("C", 3.0)]  # Contains A
    trajectories = [traj1, traj2, traj3]
    gamma = 1.0
    value = evaluate_state_value(trajectories, "A", gamma)
    # From traj1: A gives 10 + 5 = 15
    # From traj3: A gives 15 + 3 = 18
    # Average: (15 + 18) / 2 = 16.5
    expected = (15.0 + 18.0) / 2.0
    assert np.isclose(value, expected)


def test_single_state_trajectory():
    """Trajectory with only one state."""
    trajectory = [("A", 7.0)]
    value = evaluate_state_value([trajectory], "A", 0.95)
    assert np.isclose(value, 7.0)


def test_negative_rewards():
    """Should handle negative rewards."""
    trajectory = [("A", -10.0), ("B", -5.0), ("C", -3.0)]
    gamma = 0.9
    value = evaluate_state_value([trajectory], "A", gamma)
    expected = -10.0 + 0.9 * (-5.0) + 0.81 * (-3.0)
    assert np.isclose(value, expected)


def test_many_trajectories():
    """Test with many trajectories."""
    # Create 100 trajectories, each: (A, r) -> (B, r+1) with r ~ uniform [1, 10]
    np.random.seed(42)
    trajectories = []
    for _ in range(100):
        r1 = float(np.random.uniform(1, 10))
        r2 = r1 + 1.0
        trajectories.append([("A", r1), ("B", r2)])

    gamma = 0.9
    value = evaluate_state_value(trajectories, "A", gamma)

    # Manually compute expected value
    expected_values = []
    for traj in trajectories:
        g = traj[0][1] + gamma * traj[1][1]
        expected_values.append(g)
    expected = np.mean(expected_values)

    assert np.isclose(value, expected, rtol=1e-10)
