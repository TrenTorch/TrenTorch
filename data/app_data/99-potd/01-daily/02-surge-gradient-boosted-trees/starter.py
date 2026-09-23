import numpy as np


def build_regression_tree(
    X: np.ndarray,
    g: np.ndarray,
    h: np.ndarray,
    lam: float,
    gamma: float,
    max_depth: int,
    depth: int = 0,
) -> dict:
    """
    Grows ONE regularized regression tree via exact greedy split finding.

    At a node with sample set X (gradients g, hessians h) and the given
    depth: G = sum(g), H = sum(h). The node is a leaf if depth == max_depth,
    len(X) < 2, or the best candidate split's gain <= 0. A leaf's weight is
    -G / (H + lam).

    Otherwise, for every feature j and every candidate threshold t (the
    midpoint between each pair of adjacent DISTINCT values of that feature
    among these samples), split into left (x[j] <= t) and right (x[j] > t)
    and compute:

        gain(j, t) = 0.5 * (GL^2/(HL+lam) + GR^2/(HR+lam) - G^2/(H+lam)) - gamma

    where GL/HL/GR/HR are the g/h sums restricted to each side. Pick the
    (j, t) with the MAXIMUM gain; if several tie exactly, prefer the
    smallest feature index, then the smallest threshold. If that maximum
    gain is <= 0, this node is a leaf instead of splitting.

    Returns a nested dict:
      leaf:     {"leaf": True, "weight": <float>}
      internal: {"leaf": False, "feature": <int>, "threshold": <float>,
                 "left": <tree>, "right": <tree>}
    """
    pass


def gbdt_predict(
    X: np.ndarray,
    y: np.ndarray,
    T: int,
    lam: float,
    gamma: float,
    eta: float,
    max_depth: int,
    base_score: float,
    queries: np.ndarray,
) -> np.ndarray:
    """
    Trains T rounds of gradient-boosted regression trees on (X, y) with
    squared-error loss, then predicts for every row of `queries`.

    Maintain pred_i for every training sample, initialized to base_score.
    For round t = 1..T: compute g_i = pred_i - y_i (h_i is always 1.0 for
    squared error), grow one tree on the full training set via
    build_regression_tree(X, g, h, lam, gamma, max_depth), then for every
    training sample let w_i be the weight of the leaf it falls into and
    update pred_i += eta * w_i.

    To predict a query row q: route it through every tree in the order
    they were built (at each internal node go left if q[feature] <=
    threshold, else right, until reaching a leaf), and return
    base_score + eta * sum(leaf weights across all T trees).

    X: shape (n, d) training features.
    y: shape (n,) training targets.
    T: number of boosting rounds (trees).
    lam: L2 regularization on leaf weights (>= 0).
    gamma: minimum gain required to keep a split (>= 0).
    eta: learning rate / shrinkage (0 < eta <= 1).
    max_depth: maximum tree depth (root is depth 0).
    base_score: initial prediction for every sample.
    queries: shape (m, d) feature rows to predict for.
    Returns predictions, shape (m,).
    """
    pass
