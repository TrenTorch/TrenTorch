import numpy as np


def adaptive_avg_pool2d(image: np.ndarray, output_size: tuple[int, int] = (1, 1)) -> np.ndarray:
    C, H, W = image.shape
    out_h, out_w = output_size
    output = np.empty((C, out_h, out_w), dtype=image.dtype)
    for i in range(out_h):
        row_start = (i * H) // out_h
        row_end = -(-((i + 1) * H) // out_h)  # ceil division
        for j in range(out_w):
            col_start = (j * W) // out_w
            col_end = -(-((j + 1) * W) // out_w)
            window = image[:, row_start:row_end, col_start:col_end]
            output[:, i, j] = window.mean(axis=(1, 2))
    return output
