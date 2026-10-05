import numpy as np


def simulate_lunar_lander(initial_state, actions, max_steps=1000, dt=0.1):
    """
    Simulate Lunar Lander environment.

    Args:
        initial_state: [x, y, vx, vy, angle, omega, fuel]
        actions: sequence of actions (0=off, 1=left, 2=main, 3=right)
        max_steps: maximum steps
        dt: time step

    Returns:
        trajectory: list of (state, reward, done) tuples
    """
    gravity = 1.5
    main_thrust = 13.5
    side_thrust = 0.75
    initial_fuel = 1.0

    state = np.array(initial_state, dtype=np.float32)
    trajectory = []

    for t in range(min(len(actions), max_steps)):
        x, y, vx, vy, angle, omega, fuel = state

        # Check done conditions
        if y <= 0:
            # Landing condition
            if abs(vx) < 0.1 and abs(vy) < 0.1 and abs(angle) < np.pi / 4:
                trajectory.append((state.copy(), 200.0, True))
            else:
                trajectory.append((state.copy(), -100.0, True))
            break

        if fuel <= 0:
            trajectory.append((state.copy(), -100.0, True))
            break

        # Apply thruster
        action = actions[t]
        main_on = action == 2
        side = 0
        if action == 1:
            side = -1
        elif action == 3:
            side = 1

        # Compute acceleration
        thrust_x = side_thrust * side
        thrust_y = main_thrust if main_on else 0

        # Rotate thrust by angle
        ax = thrust_x * np.cos(angle) - thrust_y * np.sin(angle)
        ay = thrust_x * np.sin(angle) + thrust_y * np.cos(angle) - gravity

        # Update state
        new_vx = vx + ax * dt
        new_vy = vy + ay * dt
        new_x = x + vx * dt
        new_y = y + vy * dt

        # Simple angular dynamics
        alpha = side_thrust * side / 0.5  # Moment arm
        new_omega = omega + alpha * dt
        new_angle = angle + omega * dt

        # Fuel consumption
        new_fuel = fuel - (main_on * main_thrust + abs(side_thrust * side)) * dt / 100

        state = np.array([new_x, new_y, new_vx, new_vy, new_angle, new_omega, new_fuel], dtype=np.float32)

        trajectory.append((state.copy(), -1.0, False))

    return trajectory
