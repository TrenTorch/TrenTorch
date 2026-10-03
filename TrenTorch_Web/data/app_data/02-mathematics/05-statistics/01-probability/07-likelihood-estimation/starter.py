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


def negative_log_likelihood_normal(x: np.ndarray, mean: float, std: float) -> float:
    """
    -log(joint_density(x | mean, std)), computed in log-space (sum of
    logs) rather than as -log(product of densities): taking the log of
    a product of many small probabilities avoids the product itself
    underflowing to exactly 0.0 in floating point, the same numerical
    concern 02-cross-entropy's log_softmax addresses.

    Minimizing this over (mean, std) is EQUIVALENT to maximizing
    07-likelihood-estimation's joint_density, negating turns
    "maximize" into "minimize" and the log doesn't change which
    parameters win (log is monotonic).
    """
    pass


def mle_normal_mean(x: np.ndarray) -> float:
    """
    The maximum likelihood estimate of a Normal distribution's mean,
    given samples x. See Theory for the closed-form derivation, no
    search over candidates required.
    """
    pass


def mle_normal_std(x: np.ndarray) -> float:
    """
    The maximum likelihood estimate of a Normal distribution's std,
    given samples x. Note: this is the BIASED estimator (divides by n,
    like np.std's default, ddof=0), not 05-expectation-covariance's
    ddof=1 unbiased estimator, see Theory for why MLE gives the biased
    version specifically.
    """
    pass


def negative_log_posterior_normal(
    mean_candidate: float, x: np.ndarray, data_std: float, prior_mean: float, prior_std: float
) -> float:
    """
    -log(posterior) up to a constant, for a Normal likelihood (data_std
    assumed known) with a Normal prior on the mean:

        -log(posterior) = -log(likelihood) + -log(prior) + constant

    (Bayes' theorem's denominator, P(evidence), doesn't depend on
    mean_candidate, so it's a constant here and can be dropped when
    all you want is the ARGMIN over mean_candidate.)

    negative_log_likelihood_normal and normal_pdf are already provided
    above.
    """
    pass


def map_estimate_normal_mean(
    x: np.ndarray, data_std: float, prior_mean: float, prior_std: float
) -> float:
    """
    The closed-form MAP estimate for a Normal mean with a Normal prior:
    a precision-weighted average of the sample mean and the prior mean.
    See Theory for the exact formula and derivation sketch.
    """
    pass
