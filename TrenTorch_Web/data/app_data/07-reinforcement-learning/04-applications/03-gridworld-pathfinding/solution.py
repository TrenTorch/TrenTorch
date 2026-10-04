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
    grid = np.array(grid, dtype=np.float32)
    H, W = grid.shape

    # Initialize value function
    V = np.zeros((H, W), dtype=np.float32)
    V[goal] = 10.0

    # Action deltas: up, down, left, right
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Value iteration
    for _ in range(max_iterations):
        V_old = V.copy()

        for i in range(H):
            for j in range(W):
                if grid[i, j] == 1:  # Wall
                    V[i, j] = 0
                elif (i, j) == goal:  # Goal
                    V[i, j] = 10.0
                else:
                    # Compute best action value
                    action_values = []
                    for di, dj in deltas:
                        ni, nj = i + di, j + dj

                        # Check bounds and walls
                        if 0 <= ni < H and 0 <= nj < W and grid[ni, nj] == 0:
                            action_values.append(-1 + gamma * V_old[ni, nj])
                        else:
                            action_values.append(-1 + gamma * V_old[i, j])

                    V[i, j] = max(action_values)

    # Extract policy
    policy = np.zeros((H, W), dtype=np.int32)

    for i in range(H):
        for j in range(W):
            if grid[i, j] == 1 or (i, j) == goal:
                policy[i, j] = 0
            else:
                action_values = []
                for di, dj in deltas:
                    ni, nj = i + di, j + dj

                    if 0 <= ni < H and 0 <= nj < W and grid[ni, nj] == 0:
                        action_values.append(-1 + gamma * V[ni, nj])
                    else:
                        action_values.append(-1 + gamma * V[i, j])

                policy[i, j] = np.argmax(action_values)

    return policy
