import numpy as np


def tile_coding(state, num_tilings, num_tiles):
    """
    Tile coding feature extraction.

    Args:
        state: scalar in [0, 1]
        num_tilings: number of overlapping grids
        num_tiles: number of tiles per grid

    Returns:
        active_tiles: list of active tile indices
    """
    state = float(state)
    state = np.clip(state, 0.0, 1.0)

    active_tiles = []

    for tiling in range(num_tilings):
        # Offset for this tiling
        offset = tiling / (num_tilings * num_tiles)

        # Which tile does the (offset + state) fall into?
        position = (state + offset) % 1.0
        tile_index = int(position * num_tiles)
        tile_index = min(tile_index, num_tiles - 1)

        # Global tile index
        global_tile = tiling * num_tiles + tile_index
        active_tiles.append(global_tile)

    return active_tiles
