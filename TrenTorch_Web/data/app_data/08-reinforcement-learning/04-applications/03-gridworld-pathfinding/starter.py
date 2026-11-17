import numpy as np


def solve_gridworld(grid, start, goal, gamma=0.99, max_iterations=100):
    """
    Solve gridworld using value iteration.

    Args:
        grid: NxN array where 1=wall, 0=free
        start: (row, col) starting position
        goal: (row, col) goal position
        gamma: discount factor
        max_iterations: max VI iterations

    Returns:
        policy: NxN array of optimal actions (0=up, 1=down, 2=left, 3=right)
    """
    pass
