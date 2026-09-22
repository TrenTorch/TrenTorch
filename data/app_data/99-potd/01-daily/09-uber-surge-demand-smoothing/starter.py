def avg_pool(matrix: list[list[float]], f: int) -> list[list[float]]:
    """
    Downsample a square demand grid with non-overlapping average pooling.

    matrix: an N x N grid of floats, as a list of N rows. N is divisible by f.
    f: the window size, which is also the stride.

    Return the M x M grid (M = N // f) where cell (i, j) is the mean of the
    f x f patch of `matrix` whose top-left corner is (i * f, j * f):

        out[i][j] = mean( matrix[i*f + a][j*f + b] for 0 <= a < f, 0 <= b < f )

    Values can be negative. With f = 1 the result equals the input, and with
    f = N it is a single value, the mean of the whole grid. The grid can be
    1000 x 1000: read cells by index instead of slicing a fresh patch out of
    the grid for every window.
    """
    # TODO: see Theory for why you sum every cell in the patch before dividing
    # once by f * f, not by f.
    pass
