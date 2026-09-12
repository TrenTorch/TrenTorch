import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

Module = load_solution("03-dl-training/02-layers/05-module-base-class").Module


class TrainableModule(Module):
    def __init__(self):
        super().__init__()
        self.training = True

    def train(self, mode: bool = True) -> "TrainableModule":
        self.training = mode
        for submodule in self._modules.values():
            submodule.train(mode)
        return self

    def eval(self) -> "TrainableModule":
        return self.train(False)
