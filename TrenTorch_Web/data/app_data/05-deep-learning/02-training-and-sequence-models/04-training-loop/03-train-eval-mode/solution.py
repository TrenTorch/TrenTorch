
from _load import load_solution

Module = load_solution("dl-training-module-base-class").Module


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
