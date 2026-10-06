import numpy as np

from _load import load_solution

_module = load_solution(__file__)
simulate_cartpole = _module.simulate_cartpole


def test_basic_simulation():
    """Basic CartPole simulation."""
    initial_state = [0.0, 0.0, 0.0, 0.0]
    actions = [0, 1, 0, 1]

    trajectory = simulate_cartpole(initial_state, actions)

    assert len(trajectory) == 4
    for state, reward, done in trajectory:
        assert state.shape == (4,)
        assert reward >= 0
        assert isinstance(done, bool)


def test_done_condition():
    """Episode terminates when pole tips."""
    initial_state = [0.0, 0.0, np.pi/6, 0.0]  # Pole beyond threshold
    actions = [0]

    trajectory = simulate_cartpole(initial_state, actions)

    # Should end immediately
    assert len(trajectory) == 1
    assert trajectory[0][2] == True


def test_rewards():
    """Rewards are +1 while balanced."""
    initial_state = [0.0, 0.0, 0.0, 0.0]
    actions = [0, 0, 0]

    trajectory = simulate_cartpole(initial_state, actions)

    # All should have reward 1 unless done
    for state, reward, done in trajectory[:-1]:
        assert reward == 1.0
        assert done == False


def test_state_dimension():
    """State has correct dimension."""
    initial_state = [0.1, 0.2, 0.3, 0.4]
    actions = [0, 1]

    trajectory = simulate_cartpole(initial_state, actions)

    for state, _, _ in trajectory:
        assert len(state) == 4


def test_long_episode():
    """Long episode with stable policy."""
    initial_state = [0.0, 0.0, 0.0, 0.0]
    actions = [1, 0] * 50  # Oscillating policy

    trajectory = simulate_cartpole(initial_state, actions, max_steps=100)

    # Should have multiple steps
    assert len(trajectory) > 1
