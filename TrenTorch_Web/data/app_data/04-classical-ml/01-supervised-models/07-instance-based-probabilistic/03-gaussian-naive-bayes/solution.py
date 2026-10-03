import numpy as np


def gaussian_nb_fit(input: np.ndarray, labels: np.ndarray, var_smoothing: float = 1e-9) -> dict:
    classes = np.unique(labels)
    n_samples = input.shape[0]
    epsilon = var_smoothing * np.var(input, axis=0).max()
    log_priors, means, variances = {}, {}, {}
    for c in classes:
        mask = labels == c
        class_input = input[mask]
        log_priors[c] = float(np.log(mask.sum() / n_samples))
        means[c] = class_input.mean(axis=0)
        variances[c] = class_input.var(axis=0) + epsilon
    return {"classes": classes, "log_priors": log_priors, "means": means, "variances": variances}


def gaussian_log_likelihood(x: np.ndarray, mean: np.ndarray, variance: np.ndarray) -> float:
    return float(np.sum(-0.5 * np.log(2 * np.pi * variance) - ((x - mean) ** 2) / (2 * variance)))


def gaussian_nb_predict(model: dict, queries: np.ndarray) -> np.ndarray:
    classes = model["classes"]
    predictions = np.empty(queries.shape[0], dtype=classes.dtype)
    for i in range(queries.shape[0]):
        scores = [
            model["log_priors"][c]
            + gaussian_log_likelihood(queries[i], model["means"][c], model["variances"][c])
            for c in classes
        ]
        predictions[i] = classes[np.argmax(scores)]
    return predictions
