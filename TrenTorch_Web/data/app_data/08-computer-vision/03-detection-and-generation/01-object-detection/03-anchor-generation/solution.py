import numpy as np


def generate_anchors(fh, fw, stride, scales, ratios):
    wh = np.array([(s / np.sqrt(r), s * np.sqrt(r)) for s in scales for r in ratios])
    cy, cx = np.meshgrid((np.arange(fh) + 0.5) * stride, (np.arange(fw) + 0.5) * stride, indexing="ij")
    centres = np.stack([cx.ravel(), cy.ravel()], axis=1)
    c = centres[:, None, :]
    half = wh[None, :, :] / 2
    boxes = np.concatenate([c - half, c + half], axis=2)
    return boxes.reshape(-1, 4)
