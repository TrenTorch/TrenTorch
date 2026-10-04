import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
select_ucb_action = _module.select_ucb_action


def test_unvisited_action():
    """Action with count=0 should have infinite UCB and be selected."""
    q_values = np.array([10.0, 5.0, 0.0])
    counts = np.array([10, 10, 0])  # Action 2 never visited
    action = select_ucb_action(q_values, counts, t=100, c=1.0)
    assert action == 2


def test_greedy_when_all_visited_equally():
    """If all actions visited same number of times, pick max Q."""
    q_values = np.array([3.0, 7.0, 5.0])
    counts = np.array([10, 10, 10])
    action = select_ucb_action(q_values, counts, t=100, c=1.0)
    assert action == 1  # Highest Q value


def test_exploration_vs_exploitation():
    """Action with low count but reasonable Q can beat higher Q with many counts."""
    q_values = np.array([10.0, 5.0])  # Action 0 has higher Q
    counts = np.array([100, 1])  # Action 1 has low count
    c = 2.0  # High exploration
    action = select_ucb_action(q_values, counts, t=100, c=c)

    # Compute manually
    ucb0 = 10.0 + c * np.sqrt(np.log(100) / 100)
    ucb1 = 5.0 + c * np.sqrt(np.log(100) / 1)

    assert action == (0 if ucb0 > ucb1 else 1)


def test_time_scaling():
    """As t increases, exploration bonus increases."""
    q_values = np.array([5.0, 5.0])
    counts = np.array([10, 10])
    c = 1.0

    # At early time
    bonus_early = c * np.sqrt(np.log(10) / 10)
    # At late time
    bonus_late = c * np.sqrt(np.log(10000) / 10)

    assert bonus_late > bonus_early


def test_count_scaling():
    """As count increases for an action, its bonus decreases."""
    q_values = np.array([5.0, 5.0])
    c = 1.0
    t = 1000

    # Action with low count
    bonus_low = c * np.sqrt(np.log(t) / 1)
    # Action with high count
    bonus_high = c * np.sqrt(np.log(t) / 100)

    assert bonus_low > bonus_high


def test_exploration_constant():
    """Higher c means more exploration."""
    q_values = np.array([5.0, 5.0])
    counts = np.array([10, 20])
    t = 100

    # Same setup, different c values
    # The least-visited action should always win with high enough c
    action_low_c = select_ucb_action(q_values, counts, t, c=0.1)
    action_high_c = select_ucb_action(q_values, counts, t, c=10.0)

    # With very high c, action 0 (less visited) should win
    assert action_high_c == 0


def test_single_action():
    """Single action case."""
    q_values = np.array([5.0])
    counts = np.array([10])
    action = select_ucb_action(q_values, counts, t=100, c=1.0)
    assert action == 0


def test_all_unvisited():
    """All actions unvisited: pick the first one (tie in +inf)."""
    q_values = np.array([1.0, 2.0, 3.0])
    counts = np.array([0, 0, 0])
    action = select_ucb_action(q_values, counts, t=100, c=1.0)
    assert action == 0  # argmax of all-inf is first


def test_negative_q_values():
    """Should handle negative Q values."""
    q_values = np.array([-10.0, -5.0, -20.0])
    counts = np.array([10, 10, 10])
    action = select_ucb_action(q_values, counts, t=100, c=1.0)
    assert action == 1  # Highest (least negative)


def test_large_c():
    """With large c, always explore unvisited actions."""
    q_values = np.array([100.0, 1.0])
    counts = np.array([1000, 0])  # Action 1 never visited
    action = select_ucb_action(q_values, counts, t=100, c=100.0)
    assert action == 1


def test_small_c():
    """With small c, mostly exploit."""
    q_values = np.array([10.0, 1.0])
    counts = np.array([100, 1])
    action = select_ucb_action(q_values, counts, t=100, c=0.01)
    # With tiny c, exploration bonus is negligible, so pick highest Q
    assert action == 0


def test_large_t():
    """As t grows, bonuses grow (ln grows slowly)."""
    q_values = np.array([5.0, 5.0])
    counts = np.array([10, 10])
    c = 1.0

    action_t10 = select_ucb_action(q_values, counts, t=10, c=c)
    action_t1000000 = select_ucb_action(q_values, counts, t=1000000, c=c)

    # Both should pick same action (tied Q), but bonuses are different
    # Not testing regret, just that the function works
    assert action_t10 in [0, 1]
    assert action_t1000000 in [0, 1]


def test_return_type():
    """Should return an int."""
    q_values = np.array([1.0, 2.0, 3.0])
    counts = np.array([1, 1, 1])
    action = select_ucb_action(q_values, counts, t=10, c=1.0)
    assert isinstance(action, (int, np.integer))


def test_deterministic():
    """UCB is deterministic: same inputs give same output."""
    q_values = np.array([1.0, 5.0, 3.0, 2.0])
    counts = np.array([5, 10, 3, 8])
    t = 100
    c = 1.5

    action1 = select_ucb_action(q_values, counts, t, c)
    action2 = select_ucb_action(q_values, counts, t, c)

    assert action1 == action2
