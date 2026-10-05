import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
tile_coding = _module.tile_coding


def test_basic_tiling():
    """Basic tile coding."""
    tiles = tile_coding(state=0.5, num_tilings=2, num_tiles=4)

    assert isinstance(tiles, list)
    assert len(tiles) == 2
    assert all(isinstance(t, (int, np.integer)) for t in tiles)


def test_boundary_zero():
    """State at 0.0."""
    tiles = tile_coding(state=0.0, num_tilings=2, num_tiles=4)

    assert len(tiles) == 2
    assert all(0 <= t < 8 for t in tiles)


def test_boundary_one():
    """State at 1.0."""
    tiles = tile_coding(state=1.0, num_tilings=2, num_tiles=4)

    assert len(tiles) == 2
    assert all(0 <= t < 8 for t in tiles)


def test_range_validity():
    """All tile indices in valid range."""
    for state in np.linspace(0, 1, 10):
        tiles = tile_coding(state, num_tilings=3, num_tiles=5)
        assert all(0 <= t < 15 for t in tiles)


def test_nearby_states_share_tiles():
    """Nearby states share at least one tile."""
    tiles1 = tile_coding(state=0.5, num_tilings=2, num_tiles=4)
    tiles2 = tile_coding(state=0.51, num_tilings=2, num_tiles=4)

    # Should share at least one tile
    assert len(set(tiles1) & set(tiles2)) > 0


def test_different_tilings():
    """Different num_tilings."""
    tiles1 = tile_coding(state=0.5, num_tilings=1, num_tiles=4)
    tiles2 = tile_coding(state=0.5, num_tilings=4, num_tiles=4)

    assert len(tiles1) == 1
    assert len(tiles2) == 4


def test_different_tiles():
    """Different num_tiles."""
    tiles1 = tile_coding(state=0.5, num_tilings=2, num_tiles=2)
    tiles2 = tile_coding(state=0.5, num_tilings=2, num_tiles=8)

    # Both valid
    assert len(tiles1) == 2
    assert len(tiles2) == 2
