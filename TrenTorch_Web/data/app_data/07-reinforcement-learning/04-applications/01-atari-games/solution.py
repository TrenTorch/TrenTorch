import numpy as np
from scipy import ndimage


def preprocess_atari_frame(raw_frame):
    """
    Preprocess Atari frame for DQN.

    Args:
        raw_frame: 210x160x3 uint8 RGB frame

    Returns:
        frame: 84x84 float32 grayscale frame, normalized
    """
    raw_frame = np.array(raw_frame, dtype=np.float32)

    # Crop top and bottom (remove score bar)
    frame = raw_frame[34:194, :, :]

    # Convert to grayscale: 0.299*R + 0.587*G + 0.114*B
    gray = np.dot(frame, [0.299, 0.587, 0.114])

    # Resize to 84x84 using max-pool (2x2)
    # Simple resize via scipy
    from scipy.ndimage import zoom
    gray = zoom(gray, 84 / gray.shape[0], order=1)

    # Normalize to [0, 1]
    gray = gray / 255.0

    return gray.astype(np.float32)
