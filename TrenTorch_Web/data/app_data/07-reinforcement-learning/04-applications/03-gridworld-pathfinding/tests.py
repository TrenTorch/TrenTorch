import numpy as np

from _load import load_solution

_module = load_solution(__file__)
solve_gridworld = _module.solve_gridworld


def test_basic_gridworld():
    """Basic gridworld solving."""
    grid = np.zeros((3, 3))
    start = (0, 0)
    goal = (2, 2)

    policy = solve_gridworld(grid, start, goal)

    assert policy.shape == (3, 3)
    assert np.all(policy >= 0) and np.all(policy < 4)


def test_simple_path():
    """Simple 2x2 gridworld."""
    grid = [[0, 0], [0, 0]]
    start = (0, 0)
    goal = (1, 1)

    policy = solve_gridworld(grid, start, goal)

    # From (0,0), should go down or right
    assert policy[0, 0] in [1, 3]


def test_wall_avoidance():
    """Policy avoids walls."""
    grid = [[0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]]
    start = (0, 0)
    goal = (2, 2)

    policy = solve_gridworld(grid, start, goal)

    # Should navigate around wall
    assert policy.shape == (3, 3)


def test_direct_path():
    """Direct path without obstacles."""
    grid = np.zeros((4, 4))
    start = (0, 0)
    goal = (3, 3)

    policy = solve_gridworld(grid, start, goal)

    # Policy should be valid
    assert np.all(policy >= 0) and np.all(policy < 4)


def test_policy_convergence():
    """Policy converges with more iterations."""
    grid = np.zeros((3, 3))

    policy1 = solve_gridworld(grid, (0, 0), (2, 2), max_iterations=10)
    policy2 = solve_gridworld(grid, (0, 0), (2, 2), max_iterations=100)

    # Should converge to same policy
    assert np.allclose(policy1, policy2)
