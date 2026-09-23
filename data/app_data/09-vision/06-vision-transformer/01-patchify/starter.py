import numpy as np


def patchify(image: np.ndarray, patch_size: int) -> np.ndarray:
    """
    image: shape (C, H, W), with H and W both divisible by patch_size
    patch_size: side length of each square, non-overlapping patch

    A Vision Transformer treats an image as a "sequence" the same way a
    language transformer treats a sentence as a sequence of tokens --
    except its tokens are fixed-size square patches of pixels instead of
    words. This function is step one: cut the image into a grid of
    non-overlapping patches and flatten each patch into a single vector.

    Returns shape (num_patches, C * patch_size * patch_size), where
    num_patches = (H // patch_size) * (W // patch_size), and patches are
    ordered left-to-right, then top-to-bottom (row-major over the patch
    grid).
    """
    # TODO: reshape image (C, H, W) into (C, n_h, patch_size, n_w,
    # patch_size) where n_h = H // patch_size, n_w = W // patch_size --
    # this splits H and W into (grid position, offset within patch)
    # pairs without moving any data. Transpose to put the two grid axes
    # first: (n_h, n_w, C, patch_size, patch_size). Then reshape to
    # (n_h * n_w, C * patch_size * patch_size), flattening the patch
    # grid into a sequence and each patch's (C, patch_size, patch_size)
    # block into one vector.
    pass
