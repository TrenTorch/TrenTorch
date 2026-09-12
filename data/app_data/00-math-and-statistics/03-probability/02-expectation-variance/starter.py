import numpy as np


def sample_mean(x: np.ndarray) -> float:
    """
    The sample mean estimates a distribution's expectation E[X]:
    simply the average of the observed values.
    """
    pass


def sample_variance(x: np.ndarray, ddof: int = 0) -> float:
    """
    The sample variance estimates a distribution's Var(X). `ddof`
    ("delta degrees of freedom") controls the divisor: ddof=0 divides
    by n (the biased/population estimator), ddof=1 divides by n-1
    (Bessel's correction, the unbiased estimator). See Theory for why
    the distinction matters.
    """
    pass
