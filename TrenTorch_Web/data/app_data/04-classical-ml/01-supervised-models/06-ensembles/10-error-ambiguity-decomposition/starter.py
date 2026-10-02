import numpy as np


def ambiguity_decomposition(predictions: np.ndarray, target: np.ndarray) -> tuple:
    """
    predictions: (n_models, n_samples) regressor outputs.
    target: (n_samples,) true values.

    Returns:
        (ensemble_error, mean_individual_error, ambiguity), all mean
        squared quantities, for the simple-average ensemble.
    """
    # TODO: Compute the three quantities from their definitions.
    pass
