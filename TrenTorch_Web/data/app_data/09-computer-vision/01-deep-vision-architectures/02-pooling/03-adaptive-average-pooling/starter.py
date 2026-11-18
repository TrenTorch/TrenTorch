import numpy as np


def adaptive_avg_pool2d(image: np.ndarray, output_size: tuple[int, int] = (1, 1)) -> np.ndarray:
    """
    image: shape (C, H, W)
    output_size: (out_h, out_w) -- the exact spatial shape to produce,
    regardless of the input's own H, W

    Returns shape (C, out_h, out_w): the average of the corresponding
    region of image, per channel, for every output cell.
    """
    # TODO: For each output cell (i, j), compute which region of the
    # input it should average over using
    # start = (i * H) // out_h, end = ceil((i + 1) * H / out_h)
    # (same formula along W). Unlike 02-average-pooling, the window
    # size and stride are DERIVED from output_size, not given directly.
    pass
