import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
forward_kinematics_2d = _module.forward_kinematics_2d


def test_zero_angles():
    """Zero angles: arm extends along x-axis."""
    angles = [0.0, 0.0]
    lengths = [1.0, 1.0]

    endpoint = forward_kinematics_2d(angles, lengths)

    # Both links along x-axis
    assert np.allclose(endpoint, [2.0, 0.0], atol=1e-5)


def test_right_angle_first():
    """First joint at 90 degrees."""
    angles = [np.pi/2, 0.0]
    lengths = [1.0, 1.0]

    endpoint = forward_kinematics_2d(angles, lengths)

    # First link along y, second extends from there
    expected = [0.0, 2.0]
    assert np.allclose(endpoint, expected, atol=1e-5)


def test_opposite_angles():
    """Opposite angles cancel out."""
    angles = [np.pi/2, -np.pi/2]
    lengths = [1.0, 1.0]

    endpoint = forward_kinematics_2d(angles, lengths)

    # Should be at (0, 1)
    expected = [0.0, 1.0]
    assert np.allclose(endpoint, expected, atol=1e-5)


def test_different_lengths():
    """Different link lengths."""
    angles = [0.0, 0.0]
    lengths = [2.0, 3.0]

    endpoint = forward_kinematics_2d(angles, lengths)

    # Extends 5 units along x-axis
    assert np.allclose(endpoint, [5.0, 0.0], atol=1e-5)


def test_workspace_bounds():
    """Endpoint stays in reachable workspace."""
    angles = [np.pi/4, np.pi/4]
    lengths = [1.0, 1.0]

    endpoint = forward_kinematics_2d(angles, lengths)

    # Distance should be <= L1 + L2 = 2.0
    distance = np.linalg.norm(endpoint)
    assert distance <= 2.0 + 1e-5
