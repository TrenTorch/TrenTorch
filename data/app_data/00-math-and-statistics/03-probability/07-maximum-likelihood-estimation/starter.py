import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

normal_pdf = load_solution("00-math-and-statistics/03-probability/06-likelihood-vs-probability").normal_pdf


def negative_log_likelihood_normal(x: np.ndarray, mean: float, std: float) -> float:
    """
    -log(joint_density(x | mean, std)), computed in log-space (sum of
    logs) rather than as -log(product of densities): taking the log of
    a product of many small probabilities avoids the product itself
    underflowing to exactly 0.0 in floating point, the same numerical
    concern 02-cross-entropy's log_softmax addresses.

    Minimizing this over (mean, std) is EQUIVALENT to maximizing
    06-likelihood-vs-probability's joint_density, negating turns
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
    like np.std's default, ddof=0), not 02-expectation-variance's
    ddof=1 unbiased estimator, see Theory for why MLE gives the biased
    version specifically.
    """
    pass
