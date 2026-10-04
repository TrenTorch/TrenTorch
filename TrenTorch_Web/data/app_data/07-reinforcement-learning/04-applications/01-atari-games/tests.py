import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
preprocess_atari_frame = _module.preprocess_atari_frame


def test_basic_preprocess():
    """Basic preprocessing."""
    frame = np.random.randint(0, 256, (210, 160, 3), dtype=np.uint8)
    processed = preprocess_atari_frame(frame)

    assert processed.shape == (84, 84)
    assert processed.dtype == np.float32


def test_normalization():
    """Output normalized to [0, 1]."""
    frame = np.random.randint(0, 256, (210, 160, 3), dtype=np.uint8)
    processed = preprocess_atari_frame(frame)

    assert np.all(processed >= 0.0)
    assert np.all(processed <= 1.0)


def test_grayscale():
    """Output is 2D (grayscale)."""
    frame = np.random.randint(0, 256, (210, 160, 3), dtype=np.uint8)
    processed = preprocess_atari_frame(frame)

    assert len(processed.shape) == 2


def test_consistent():
    """Same input gives same output."""
    frame = np.ones((210, 160, 3), dtype=np.uint8) * 128

    processed1 = preprocess_atari_frame(frame)
    processed2 = preprocess_atari_frame(frame)

    assert np.allclose(processed1, processed2)


def test_black_frame():
    """All black frame."""
    frame = np.zeros((210, 160, 3), dtype=np.uint8)
    processed = preprocess_atari_frame(frame)

    assert np.allclose(processed, 0.0)


def test_white_frame():
    """All white frame."""
    frame = np.ones((210, 160, 3), dtype=np.uint8) * 255
    processed = preprocess_atari_frame(frame)

    assert np.allclose(processed, 1.0)
