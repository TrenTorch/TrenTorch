import numpy as np


class ArrayDataset:
    """
    The simplest possible Dataset: wraps two parallel NumPy arrays
    (features and targets) and exposes them index-by-index, matching
    PyTorch's Dataset contract: `__len__` and `__getitem__`.
    """

    def __init__(self, features: np.ndarray, targets: np.ndarray):
        self.features = features
        self.targets = targets

    def __len__(self) -> int:
        pass

    def __getitem__(self, idx: int):
        pass


class DataLoader:
    """
    Wraps a Dataset (anything supporting __len__ and __getitem__) and
    iterates over it in BATCHES, optionally shuffling the order once per
    full pass (once per `for batch in loader:` loop), using `seed` for
    reproducibility.
    """

    def __init__(self, dataset, batch_size: int, shuffle: bool = False, seed: int | None = None):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.seed = seed

    def __iter__(self):
        """
        Yields (batch_features, batch_targets) pairs, each a stacked
        NumPy array of up to `batch_size` samples, until every sample in
        the dataset has been yielded exactly once (the LAST batch may be
        smaller than batch_size if the dataset size doesn't divide evenly).
        """
        pass

    def __len__(self) -> int:
        """The number of batches one full pass produces."""
        pass
