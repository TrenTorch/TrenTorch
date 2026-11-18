import numpy as np


def zero_shot_predict(img_emb, class_embs):
    img = np.asarray(img_emb, dtype=float)
    cls = np.asarray(class_embs, dtype=float)
    img = img / np.linalg.norm(img)
    cls = cls / np.linalg.norm(cls, axis=1, keepdims=True)
    return int(np.argmax(cls @ img))
