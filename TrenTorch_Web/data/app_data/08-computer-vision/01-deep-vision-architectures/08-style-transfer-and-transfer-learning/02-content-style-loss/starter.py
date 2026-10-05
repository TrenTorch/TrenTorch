import numpy as np


def content_loss(gen_feat: np.ndarray, content_feat: np.ndarray) -> float:
    """Mean squared error between feature maps."""
    # TODO
    pass


def style_loss(gen_feats: list[np.ndarray], style_feats: list[np.ndarray], layer_weights: list[float]) -> float:
    """Weighted sum over layers of the MSE between Gram matrices."""
    # TODO
    pass


def total_loss(content: float, style: float, tv: float, w_content: float, w_style: float, w_tv: float) -> float:
    """Weighted sum of the three terms."""
    # TODO
    pass
