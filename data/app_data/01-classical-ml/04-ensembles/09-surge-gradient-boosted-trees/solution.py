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
    n = X.shape[0]
    G = float(np.sum(g))
    H = float(np.sum(h))

    def leaf():
        return {"leaf": True, "weight": -G / (H + lam)}

    if depth == max_depth or n < 2:
        return leaf()

    d = X.shape[1]
    parent_term = (G * G) / (H + lam)

    best_gain = -np.inf
    best_feature = None
    best_threshold = None

    for j in range(d):
        values = np.unique(X[:, j])
        if values.shape[0] < 2:
            continue
        for a, b in zip(values[:-1], values[1:]):
            t = (a + b) / 2.0
            left_mask = X[:, j] <= t
            GL = float(np.sum(g[left_mask]))
            HL = float(np.sum(h[left_mask]))
            GR = G - GL
            HR = H - HL
            gain = 0.5 * ((GL * GL) / (HL + lam) + (GR * GR) / (HR + lam) - parent_term) - gamma
            if gain > best_gain:
                best_gain = gain
                best_feature = j
                best_threshold = t

    if best_feature is None or best_gain <= 0:
        return leaf()

    left_mask = X[:, best_feature] <= best_threshold
    right_mask = ~left_mask
    return {
        "leaf": False,
        "feature": best_feature,
        "threshold": best_threshold,
        "left": build_regression_tree(
            X[left_mask], g[left_mask], h[left_mask], lam, gamma, max_depth, depth + 1
        ),
        "right": build_regression_tree(
            X[right_mask], g[right_mask], h[right_mask], lam, gamma, max_depth, depth + 1
        ),
    }


def _route(tree: dict, x: np.ndarray) -> float:
    node = tree
    while not node["leaf"]:
        node = node["left"] if x[node["feature"]] <= node["threshold"] else node["right"]
    return node["weight"]


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
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    queries = np.asarray(queries, dtype=float)
    n = X.shape[0]

    pred = np.full(n, float(base_score))
    trees = []
    for _ in range(T):
        g = pred - y
        h = np.ones(n)
        tree = build_regression_tree(X, g, h, lam, gamma, max_depth)
        trees.append(tree)
        weights = np.array([_route(tree, X[i]) for i in range(n)])
        pred = pred + eta * weights

    m = queries.shape[0]
    out = np.full(m, float(base_score))
    for tree in trees:
        weights = np.array([_route(tree, queries[i]) for i in range(m)])
        out = out + eta * weights
    return out
