import math


def decode_xy(sx, sy, col, row, S, img):
    """
    sx, sy: raw network outputs for the box centre offset within its cell
    col, row: grid cell of the box
    S: number of grid cells per side
    img: image side length in pixels

    Returns:
        The box centre (x, y) in pixels, with the offset kept inside the cell by a sigmoid.
    """
    # TODO: Squash the raw offsets to (0, 1), add them to the cell position, and scale to pixels (see Theory).
    pass
