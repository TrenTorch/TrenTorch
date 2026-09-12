import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

Module = load_solution("03-dl-training/02-layers/05-module-base-class").Module


class TrainableModule(Module):
    """
    Extends `[02-layers/05-module-base-class]`'s Module with a
    `self.training` flag, and `train()`/`eval()` methods that flip it,
    recursively, for this module AND every child module (and their
    children, to any depth), matching torch.nn.Module's train()/eval().
    """

    def __init__(self):
        super().__init__()
        self.training = True

    def train(self, mode: bool = True) -> "TrainableModule":
        """
        Sets self.training = mode on THIS module, and recursively calls
        train(mode) on every child in self._modules too. Returns self
        (so calls like `model.train()` can be chained, matching
        PyTorch's convention).
        """
        pass

    def eval(self) -> "TrainableModule":
        """Equivalent to train(False)."""
        pass
