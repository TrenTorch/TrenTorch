import numpy as np


def bernoulli_nb_fit(input: np.ndarray, labels: np.ndarray, alpha: float = 1.0) -> dict:
    classes = np.unique(labels)
    n_samples = input.shape[0]
    log_priors = {}
    feature_probs = {}
    for c in classes:
        mask = labels == c
        class_count = mask.sum()
        log_priors[c] = float(np.log(class_count / n_samples))
        feature_probs[c] = (input[mask].sum(axis=0) + alpha) / (class_count + 2 * alpha)
    return {"classes": classes, "log_priors": log_priors, "feature_probs": feature_probs}


def bernoulli_log_likelihood(x: np.ndarray, feature_probs: np.ndarray) -> float:
    return float(np.sum(x * np.log(feature_probs) + (1 - x) * np.log(1 - feature_probs)))


def bernoulli_nb_predict(model: dict, queries: np.ndarray) -> np.ndarray:
    classes = model["classes"]
    predictions = np.empty(queries.shape[0], dtype=classes.dtype)
    for i in range(queries.shape[0]):
        scores = [
            model["log_priors"][c]
            + bernoulli_log_likelihood(queries[i], model["feature_probs"][c])
            for c in classes
        ]
        predictions[i] = classes[np.argmax(scores)]
    return predictions
