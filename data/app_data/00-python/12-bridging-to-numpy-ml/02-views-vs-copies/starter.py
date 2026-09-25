class View:
    """
    A window onto a shared list.

    __init__(self, buffer, indices=None):
        Store `buffer` (the list itself: do NOT copy it) in
        self.buffer. Store `indices`, a range object listing which
        buffer positions this view exposes, in self.indices. If
        `indices` is None, use range(len(buffer)).

    __len__(self):
        Return the number of positions in the view.

    __getitem__(self, key):
        If `key` is an int, return the buffer value at position
        self.indices[key] (negative keys allowed; out-of-range
        raises IndexError, as indexing a range does). If `key` is
        a slice, return a NEW View of the SAME buffer whose
        indices are self.indices[key].

    __setitem__(self, key, value):
        `key` is an int. Store `value` in the buffer at position
        self.indices[key]. The change must be visible through
        every view of that buffer.

    to_list(self):
        Return a NEW list containing the values this view exposes,
        in order. Changing the returned list must not change the
        buffer.
    """

    def __init__(self, buffer, indices=None):
        pass

    def __len__(self):
        pass

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def to_list(self):
        pass


def shares_buffer(a, b) -> bool:
    """
    Return True if the two View objects use the exact same buffer
    object (identity, `is`), even if they expose different
    positions.
    """
    pass


def scale_in_place(view, k) -> None:
    """
    Multiply every value that `view` exposes by `k`, writing the
    results back into the buffer (through the view). Return
    nothing.
    """
    pass


def scaled_copy(view, k) -> list:
    """
    Return a NEW list of every value `view` exposes multiplied by
    `k`. The buffer must not change.
    """
    pass
