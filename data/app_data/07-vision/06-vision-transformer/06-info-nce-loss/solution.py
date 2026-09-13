import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

softmax = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax
cce_loss = load_solution("01-classical-ml/02-classification/06-softmax-cce").cce_loss


def info_nce_loss(image_embeds: np.ndarray, text_embeds: np.ndarray, temperature: float = 0.07) -> float:
    image_norm = image_embeds / np.linalg.norm(image_embeds, axis=1, keepdims=True)
    text_norm = text_embeds / np.linalg.norm(text_embeds, axis=1, keepdims=True)

    logits = (image_norm @ text_norm.T) / temperature
    n = logits.shape[0]
    labels = np.arange(n)

    loss_image_to_text = cce_loss(softmax(logits), labels)
    loss_text_to_image = cce_loss(softmax(logits.T), labels)
    return float((loss_image_to_text + loss_text_to_image) / 2.0)
