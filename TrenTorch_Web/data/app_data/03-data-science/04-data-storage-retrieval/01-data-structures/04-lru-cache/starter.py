class LRUCache:
    """
    A least-recently-used cache with O(1) get and put, built from a dict
    and a doubly linked list you write yourself. Do not use OrderedDict.
    """

    def __init__(self, capacity: int):
        """capacity >= 1 is the maximum number of entries."""
        # TODO: Create the dict and the sentinel nodes of the linked list.
        pass

    def get(self, key):
        """
        Returns the value and marks the key most recently used. Returns
        None, changing nothing, if the key is absent.
        """
        # TODO: Find the node, move it to the front, return its value.
        pass

    def put(self, key, value) -> None:
        """
        Stores key -> value as the most recently used entry. Replaces the
        value of an existing key. If a NEW key would exceed the capacity,
        evicts the least recently used entry first.
        """
        # TODO: Update or insert, evicting from the tail when over capacity.
        pass

    def __len__(self) -> int:
        """Returns the number of entries."""
        # TODO: Return the size of the dict.
        pass

    def keys_by_recency(self) -> list:
        """Returns all keys from most to least recently used."""
        # TODO: Walk the list from the head to the tail.
        pass
