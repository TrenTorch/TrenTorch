def max_pool(matrix: list[list[float]], f: int) -> list[list[float]]:
    """
    Downsample a square feature map with non-overlapping max pooling.

    matrix: an N x N grid of floats, as a list of N rows. N is divisible by f.
    f: the window size, which is also the stride.

    Return the M x M grid (M = N // f) where cell (i, j) is the maximum of the
    f x f patch of `matrix` whose top-left corner is (i * f, j * f):

        out[i][j] = max( matrix[i*f + a][j*f + b] for 0 <= a < f, 0 <= b < f )

    Values can all be negative, so do not start a running maximum at 0.0. With
    f = 1 the result equals the input, and with f = N it is a single value.
    The grid can be 1000 x 1000: read cells by index instead of copying a
    slice for every window.
    """
    # TODO: see Theory for how to pick the starting value of the running maximum.
    pass
