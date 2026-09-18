import numpy as np


def pca_fit(input: np.ndarray, n_components: int) -> dict:
    mean = input.mean(axis=0)
    centered = input - mean

    _, singular_values, components_t = np.linalg.svd(centered, full_matrices=False)
    components = components_t[:n_components]

    # Deterministic sign convention (matches scikit-learn's svd_flip):
    # for each component, make the largest-magnitude coefficient positive.
    max_abs_idx = np.argmax(np.abs(components), axis=1)
    signs = np.sign(components[np.arange(components.shape[0]), max_abs_idx])
    components = components * signs[:, np.newaxis]

    n_samples = input.shape[0]
    explained_variance = (singular_values[:n_components] ** 2) / (n_samples - 1)

    return {"mean": mean, "components": components, "explained_variance": explained_variance}


def pca_transform(model: dict, input: np.ndarray) -> np.ndarray:
    return (input - model["mean"]) @ model["components"].T
