class MinHeap:
    """A binary min-heap in a plain list. Do not use heapq."""

    def __init__(self):
        """Starts empty. The items live in the list `self.items`."""
        # TODO: Create the empty item list.
        pass

    def push(self, x) -> None:
        """Appends x and sifts it up while it is smaller than its parent."""
        # TODO: Append, then restore the heap property upward.
        pass

    def pop(self):
        """
        Removes and returns the smallest item. Moves the last item to the
        root and sifts it down toward the smaller child.
        Raises IndexError on an empty heap.
        """
        # TODO: Take the root, then restore the heap property downward.
        pass

    def peek(self):
        """Returns the smallest item without removing it. IndexError if empty."""
        # TODO: Return the root.
        pass

    def __len__(self) -> int:
        """Returns the number of items."""
        # TODO: Return the number of stored items.
        pass


def heapify(values: list) -> MinHeap:
    """
    Returns a new MinHeap holding all of `values`, built by sifting down
    from the last parent to the root (not by n pushes). `values` must
    not be modified.
    """
    # TODO: Build the heap in linear time.
    pass


def top_k(stream, k: int) -> list:
    """
    Consumes the iterable once and returns its k largest values in
    descending order, keeping a MinHeap of at most k items. Returns fewer
    if the stream is shorter, and [] when k <= 0.
    """
    # TODO: Keep the best k seen so far in a min-heap.
    pass


def merge_sorted(lists: list) -> list:
    """
    Merges several sorted lists into one sorted list using a heap that
    holds at most one entry per list. Ties keep the order of the lists.
    Do not sort the combined list.
    """
    # TODO: Repeatedly pop the smallest head and push its successor.
    pass
