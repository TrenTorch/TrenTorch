import numpy as np


def normal_pdf(x: np.ndarray, mean: float, std: float) -> np.ndarray:
    """
    The Normal (Gaussian) probability density function:

        pdf(x) = (1 / (std * sqrt(2*pi))) * exp(-0.5 * ((x - mean) / std)^2)
    """
    pass


def joint_density(x_values: np.ndarray, mean: float, std: float) -> float:
    """
    Assuming every value in x_values is drawn independently from the
    same Normal(mean, std), their joint density is the product of each
    one's individual density (independent events multiply).
    """
    pass


def likelihood_curve(x_values: np.ndarray, candidate_means: np.ndarray, std: float) -> np.ndarray:
    """
    The SAME joint_density formula, but now x_values is held fixed
    (it's your one, already-observed dataset) and `mean` is swept
    across every value in `candidate_means` instead. Returns one joint
    density value per candidate mean, this array IS the likelihood
    function, viewed as a curve over possible parameter values.
    """
    pass
