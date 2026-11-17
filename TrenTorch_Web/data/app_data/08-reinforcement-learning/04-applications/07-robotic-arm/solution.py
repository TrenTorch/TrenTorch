import numpy as np


def forward_kinematics_2d(joint_angles, link_lengths):
    """
    Compute end-effector position from joint angles.

    Args:
        joint_angles: [theta1, theta2] in radians
        link_lengths: [L1, L2]

    Returns:
        endpoint: (x, y) position
    """
    theta1, theta2 = joint_angles
    L1, L2 = link_lengths

    # First link endpoint
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)

    # Second link relative angle
    theta2_abs = theta1 + theta2

    # Second link endpoint (absolute position)
    x = x1 + L2 * np.cos(theta2_abs)
    y = y1 + L2 * np.sin(theta2_abs)

    return np.array([x, y], dtype=np.float32)
