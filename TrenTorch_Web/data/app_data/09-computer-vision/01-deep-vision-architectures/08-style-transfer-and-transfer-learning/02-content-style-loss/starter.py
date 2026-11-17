import numpy as np


def _gram(feat: np.ndarray) -> np.ndarray:
    """Gram matrix of one (C, H, W) feature map: F @ F.T / (C * H * W), with F = feat.reshape(C, -1)."""
    # TODO
    pass


def content_loss(gen_feat: np.ndarray, content_feat: np.ndarray) -> float:
    """Mean squared error between feature maps."""
    # TODO
    pass


def style_loss(gen_feats: list[np.ndarray], style_feats: list[np.ndarray], layer_weights: list[float]) -> float:
    """Weighted sum over layers of the MSE between Gram matrices. Use _gram for both images."""
    # TODO
    pass


def total_loss(content: float, style: float, tv: float, w_content: float, w_style: float, w_tv: float) -> float:
    """Weighted sum of the three terms."""
    # TODO
    pass
