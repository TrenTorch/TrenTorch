import numpy as np


def clip_logits(img, txt, temp):
    img = np.asarray(img, dtype=float)
    txt = np.asarray(txt, dtype=float)
    img = img / np.linalg.norm(img, axis=1, keepdims=True)
    txt = txt / np.linalg.norm(txt, axis=1, keepdims=True)
    return (img @ txt.T) / temp
