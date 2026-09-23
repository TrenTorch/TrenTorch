import numpy as np


class MetricTracker:
    def __init__(self):
        self.history: dict[str, list[float]] = {}

    def record(self, name: str, value: float) -> None:
        self.history.setdefault(name, []).append(value)

    def get_history(self, name: str) -> list[float]:
        return self.history.get(name, [])

    def moving_average(self, name: str, window: int) -> list[float]:
        values = self.history.get(name, [])
        result = []
        for i in range(len(values)):
            start = max(0, i - window + 1)
            result.append(float(np.mean(values[start : i + 1])))
        return result

    def best(self, name: str, mode: str = "min") -> float | None:
        values = self.history.get(name, [])
        if not values:
            return None
        return min(values) if mode == "min" else max(values)
