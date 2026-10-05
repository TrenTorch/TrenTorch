import math


class BloomFilter:
    def __init__(self, num_bits: int, num_hashes: int):
        self.num_bits = num_bits
        self.num_hashes = num_hashes
        self.bits = [0] * num_bits

    def _positions(self, item: int) -> list:
        h1 = (item * 2654435761) % 2**32
        h2 = ((item * 40503) % 2**32) | 1
        return [(h1 + i * h2) % self.num_bits for i in range(self.num_hashes)]

    def add(self, item: int) -> None:
        for position in self._positions(item):
            self.bits[position] = 1

    def might_contain(self, item: int) -> bool:
        return all(self.bits[position] == 1 for position in self._positions(item))


def false_positive_rate(num_items: int, num_bits: int, num_hashes: int) -> float:
    return float((1.0 - math.exp(-num_hashes * num_items / num_bits)) ** num_hashes)


def optimal_num_hashes(num_bits: int, num_items: int) -> int:
    return max(1, int(round((num_bits / num_items) * math.log(2))))
