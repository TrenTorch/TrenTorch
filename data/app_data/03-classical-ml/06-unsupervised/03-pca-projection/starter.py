import numpy as np


def pca_fit(input: np.ndarray, n_components: int) -> dict:
    """
    Returns a dict:
      "mean": array (n_features,), the training data's mean.
      "components": array (n_components, n_features), the top
        principal directions, each a unit vector, sorted by how much
        variance they capture (most first). Sign is fixed by making
        each component's largest-magnitude coefficient positive.
      "explained_variance": array (n_components,), the variance of the
        (centered) data along each component.
    """
    # TODO: mean = input.mean(axis=0), centered = input - mean.
    # np.linalg.svd(centered, full_matrices=False) gives (U, S, Vt).
    # components = Vt[:n_components].
    # Sign fix: for each row of components, find the index of its
    # largest-magnitude entry, flip the whole row's sign so that entry
    # is positive.
    # explained_variance = singular_values[:n_components]**2 / (n_samples - 1)
    pass


def pca_transform(model: dict, input: np.ndarray) -> np.ndarray:
    """
    Returns:
        shape (n_samples, n_components): input projected onto the
        principal components (centered first, using the SAME mean the
        model was fit with, not this input's own mean).
    """
    # TODO: (input - model["mean"]) @ model["components"].T
    pass
