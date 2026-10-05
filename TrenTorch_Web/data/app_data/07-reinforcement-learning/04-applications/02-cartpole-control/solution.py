import numpy as np


def simulate_cartpole(initial_state, actions, max_steps=500, dt=0.02):
    """
    Simulate CartPole environment.

    Args:
        initial_state: [x, v_x, theta, omega]
        actions: sequence of actions (0=left, 1=right)
        max_steps: maximum simulation steps
        dt: time step

    Returns:
        trajectory: list of (state, reward, done) tuples
    """
    # Physics parameters
    gravity = 9.8
    cart_mass = 1.0
    pole_mass = 0.1
    pole_length = 0.5
    force_mag = 10.0

    state = np.array(initial_state, dtype=np.float32)
    trajectory = []

    for t in range(min(len(actions), max_steps)):
        x, v_x, theta, omega = state

        # Check done
        if abs(x) > 2.4 or abs(theta) > np.pi / 12:
            trajectory.append((state.copy(), 0.0, True))
            break

        # Apply force based on action
        force = force_mag if actions[t] == 1 else -force_mag

        # CartPole dynamics (simplified Euler)
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)

        denom = cart_mass + pole_mass * sin_theta ** 2
        acc_x = (force + pole_mass * pole_length * omega ** 2 * sin_theta) / denom
        acc_theta = (gravity * sin_theta - cos_theta * acc_x) / pole_length

        # Update state
        state = np.array([
            x + v_x * dt,
            v_x + acc_x * dt,
            theta + omega * dt,
            omega + acc_theta * dt
        ], dtype=np.float32)

        trajectory.append((state.copy(), 1.0, False))

    return trajectory
