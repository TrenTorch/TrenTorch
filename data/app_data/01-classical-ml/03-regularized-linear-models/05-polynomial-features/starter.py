from itertools import combinations_with_replacement

import numpy as np


def polynomial_features_multivariate(X: np.ndarray, degree: int) -> np.ndarray:
    """
    `07-evaluation/03-bias-variance-tradeoff`'s own polynomial_features
    handles a SINGLE input variable. This generalizes to MULTIPLE input
    features, including every INTERACTION term (products of different
    features), not just pure powers of one feature at a time.

    X: (n, num_features). Returns (n, num_monomials), every monomial
    of total degree 0 through `degree`, built from every
    combinations_with_replacement of feature indices, in that exact
    order (matching sklearn.preprocessing.PolynomialFeatures'
    column ordering, degree 0 first, then degree 1, degree 2, and so
    on, each degree's monomials in combinations_with_replacement order).

    `itertools.combinations_with_replacement` is already imported above.
    """
    pass
