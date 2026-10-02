import numpy as np


def normal_pdf(x: np.ndarray, mean: float, std: float) -> np.ndarray:
    coefficient = 1.0 / (std * np.sqrt(2.0 * np.pi))
    exponent = -0.5 * ((x - mean) / std) ** 2
    return coefficient * np.exp(exponent)


def joint_density(x_values: np.ndarray, mean: float, std: float) -> float:
    return float(np.prod(normal_pdf(x_values, mean, std)))


def likelihood_curve(x_values: np.ndarray, candidate_means: np.ndarray, std: float) -> np.ndarray:
    return np.array([joint_density(x_values, mean, std) for mean in candidate_means])


def negative_log_likelihood_normal(x: np.ndarray, mean: float, std: float) -> float:
    return float(-np.sum(np.log(normal_pdf(x, mean, std))))


def mle_normal_mean(x: np.ndarray) -> float:
    return float(np.mean(x))


def mle_normal_std(x: np.ndarray) -> float:
    mean = mle_normal_mean(x)
    return float(np.sqrt(np.mean((x - mean) ** 2)))


def negative_log_posterior_normal(
    mean_candidate: float, x: np.ndarray, data_std: float, prior_mean: float, prior_std: float
) -> float:
    nll = negative_log_likelihood_normal(x, mean_candidate, data_std)
    neg_log_prior = float(-np.log(normal_pdf(np.array([mean_candidate]), prior_mean, prior_std))[0])
    return nll + neg_log_prior


def map_estimate_normal_mean(
    x: np.ndarray, data_std: float, prior_mean: float, prior_std: float
) -> float:
    n = len(x)
    sample_mean = np.mean(x)
    data_precision = n / data_std**2
    prior_precision = 1.0 / prior_std**2
    return float(
        (data_precision * sample_mean + prior_precision * prior_mean)
        / (data_precision + prior_precision)
    )
