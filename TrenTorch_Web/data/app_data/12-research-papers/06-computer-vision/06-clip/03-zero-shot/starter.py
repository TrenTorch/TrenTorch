import numpy as np


def zero_shot_predict(img_emb, class_embs):
    """
    img_emb: embedding of one image, shape (d,)
    class_embs: embedding of each class's text prompt, shape (C, d)

    Returns:
        The index of the class whose prompt embedding is most similar to the image, as a Python int.
    """
    # TODO: Normalize the embeddings and return the class with the highest cosine similarity (see Theory).
    pass
