import numpy as np


def project(a, b):
    """
    a, b: 1D NumPy arrays of the same length; b is never the zero vector

    Returns:
        The projection of a onto b: the component of a pointing along
        b's direction, as a vector (a scaled copy of b).
    """
    # TODO: Implement proj_b(a) = ((a . b) / (b . b)) * b from Theory.
    pass


def orthogonal_component(a, b):
    """
    a, b: same as project(a, b)

    Returns:
        The component of a perpendicular to b -- what's left of a after
        removing its projection onto b.
    """
    # TODO: Implement using project(a, b) from Theory.
    pass
