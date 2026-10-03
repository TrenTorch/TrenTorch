import numpy as np


class MinMaxScaler:
    """
    Scales each column to [0, 1] using the training minimum and maximum.
    A column with zero training range maps every value to 0.
    """

    def fit(self, X: np.ndarray) -> "MinMaxScaler":
        pass

    def transform(self, X: np.ndarray) -> np.ndarray:
        pass

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        pass


class Pipeline:
    """
    Runs a list of transformers in order. fit_transform fits each step
    on the output of the previous one. transform replays the fitted steps.
    """

    def __init__(self, steps: list) -> None:
        pass

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        pass

    def transform(self, X: np.ndarray) -> np.ndarray:
        pass
