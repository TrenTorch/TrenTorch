import numpy as np


def simulate_mountain_car(initial_state, actions, max_steps=500, dt=0.1):
    """
    Simulate Mountain Car environment.

    Args:
        initial_state: [position, velocity]
        actions: sequence of actions (-1, 0, or 1)
        max_steps: maximum steps
        dt: time step

    Returns:
        trajectory: list of (state, reward, done) tuples
    """
    gravity = 0.0025
    friction = 0.01
    max_position = 0.6
    min_position = -1.2
    max_velocity = 0.07

    state = np.array(initial_state, dtype=np.float32)
    trajectory = []

    for t in range(min(len(actions), max_steps)):
        position, velocity = state

        # Goal condition
        if position >= max_position:
            trajectory.append((state.copy(), 10.0, True))
            break

        # Apply action
        action = actions[t]

        # Physics: v' = v + (action - gravity - friction*v)*dt
        acceleration = action - gravity * np.cos(position) - friction * velocity
        new_velocity = np.clip(velocity + acceleration * dt, -max_velocity, max_velocity)
        new_position = np.clip(position + new_velocity * dt, min_position, max_position)

        state = np.array([new_position, new_velocity], dtype=np.float32)

        trajectory.append((state.copy(), -1.0, False))

    return trajectory
