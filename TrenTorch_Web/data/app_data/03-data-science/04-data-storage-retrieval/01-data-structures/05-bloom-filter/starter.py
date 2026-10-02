import math


class BloomFilter:
    """
    A Bloom filter over non-negative integer items.
    Base hashes: h1 = (item * 2654435761) % 2**32 and
    h2 = ((item * 40503) % 2**32) | 1. The i-th bit position of an item
    is (h1 + i * h2) % num_bits for i = 0 .. num_hashes - 1.
    """

    def __init__(self, num_bits: int, num_hashes: int):
        """Creates num_bits bits (a plain list of 0 and 1), all zero."""
        # TODO: Store the sizes and the bit list.
        pass

    def add(self, item: int) -> None:
        """Sets the item's num_hashes bit positions to 1."""
        # TODO: Compute the positions and switch them on.
        pass

    def might_contain(self, item: int) -> bool:
        """
        Returns True only if every one of the item's bit positions is 1.
        Never modifies the filter.
        """
        # TODO: Check all of the item's positions.
        pass


def false_positive_rate(num_items: int, num_bits: int, num_hashes: int) -> float:
    """Returns (1 - exp(-num_hashes * num_items / num_bits)) ** num_hashes."""
    # TODO: Implement the formula from Theory.
    pass


def optimal_num_hashes(num_bits: int, num_items: int) -> int:
    """Returns max(1, round((num_bits / num_items) * ln 2)) as an int."""
    # TODO: Implement k = (m / n) ln 2.
    pass
