import numpy as np


class ArrayDataset:
    def __init__(self, features: np.ndarray, targets: np.ndarray):
        self.features = features
        self.targets = targets

    def __len__(self) -> int:
        return len(self.features)

    def __getitem__(self, idx: int):
        return self.features[idx], self.targets[idx]


class DataLoader:
    def __init__(self, dataset, batch_size: int, shuffle: bool = False, seed: int | None = None):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.seed = seed

    def __iter__(self):
        indices = np.arange(len(self.dataset))
        if self.shuffle:
            rng = np.random.RandomState(self.seed)
            rng.shuffle(indices)

        for start in range(0, len(indices), self.batch_size):
            batch_indices = indices[start : start + self.batch_size]
            batch_x = np.stack([self.dataset[i][0] for i in batch_indices])
            batch_y = np.stack([self.dataset[i][1] for i in batch_indices])
            yield batch_x, batch_y

    def __len__(self) -> int:
        return (len(self.dataset) + self.batch_size - 1) // self.batch_size
