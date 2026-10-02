class HashTable:
    """A hash table with separate chaining. Do not use dict or set inside."""

    def __init__(self, capacity: int = 8):
        """Creates `capacity` empty buckets. `capacity` stays readable."""
        # TODO: Create the buckets and start the size at 0.
        pass

    def put(self, key, value) -> None:
        """
        Stores key -> value in bucket hash(key) % capacity, replacing the
        value if the key exists. After adding a NEW key, if load_factor()
        is above 0.75, double the capacity and rehash every pair.
        """
        # TODO: Find the bucket, update or append, then grow if too full.
        pass

    def get(self, key, default=None):
        """Returns the stored value, or `default` if the key is absent."""
        # TODO: Scan the one bucket the key can be in.
        pass

    def delete(self, key) -> bool:
        """Removes the key. Returns True if it was present, else False."""
        # TODO: Remove the pair from its bucket.
        pass

    def __len__(self) -> int:
        """Returns the number of stored keys."""
        # TODO: Return the size.
        pass

    def load_factor(self) -> float:
        """Returns len(self) / capacity as a float."""
        # TODO: Divide the size by the capacity.
        pass

    def keys(self) -> list:
        """Returns a list of all keys, in any order."""
        # TODO: Collect the keys from every bucket.
        pass
