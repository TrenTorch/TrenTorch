import numpy as np


class MinMaxScaler:
    def fit(self, X: np.ndarray) -> "MinMaxScaler":
        X = np.asarray(X, dtype=float)
        self.min_ = X.min(axis=0)
        self.max_ = X.max(axis=0)
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        span = np.where(self.max_ - self.min_ == 0, np.inf, self.max_ - self.min_)
        return (X - self.min_) / span

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


class Pipeline:
    def __init__(self, steps: list) -> None:
        self.steps = list(steps)

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        for step in self.steps:
            X = step.fit_transform(X)
        return X

    def transform(self, X: np.ndarray) -> np.ndarray:
        for step in self.steps:
            X = step.transform(X)
        return X
