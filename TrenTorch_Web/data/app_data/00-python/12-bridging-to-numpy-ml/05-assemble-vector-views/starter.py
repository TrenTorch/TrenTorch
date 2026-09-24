import math


class Vector:
    """
    A one-dimensional sequence of numbers that can be a view onto
    shared data.

    __init__(self, buffer, indices=None):
        Store `buffer` (a list; do NOT copy it) in self.buffer.
        Store `indices` (a range of buffer positions) in
        self.indices; if None, use range(len(buffer)).

    __len__(self):
        Number of positions exposed.

    __getitem__(self, key):
        int   -> the element at that position of the view
                 (negative allowed; out of range raises
                 IndexError).
        slice -> a NEW Vector that is a VIEW of the same buffer
                 (indices = self.indices[key]).

    __setitem__(self, key, value):
        int   -> write `value` into the buffer at that position.
        slice -> `value` is either a single number, written to
                 EVERY selected position, or a sequence (anything
                 with a length) whose elements are written to the
                 selected positions in order. Take a snapshot
                 list of a sequence value BEFORE writing, so
                 overlapping source and target cannot corrupt
                 each other. The lengths must match for a
                 sequence value.
        Writes go into the buffer and are visible through every
        view of it.

    to_list(self):
        A NEW list of the exposed values.

    copy(self):
        A NEW Vector that owns a NEW buffer holding the exposed
        values (independent of this one).

    map(self, func):
        A NEW Vector (new buffer) holding func(x) for every
        exposed x.

    __add__(self, other):
        `other` is either a number (add it to every element) or a
        sequence with a length, such as another Vector or a list
        (add element-wise; equal lengths). Return a NEW Vector
        with a NEW buffer. Decide scalar vs sequence with
        hasattr(other, "__len__"), not isinstance.

    __radd__(self, other):
        Return self + other, so sum([...vectors...]) works.

    normalize_(self, eps=1e-5):
        Layer-normalize the exposed values IN PLACE: with
        mean = sum/n and variance = sum((x - mean)**2)/n, write
        (x - mean) / sqrt(variance + eps) back into the buffer
        at the exposed positions. Positions outside the view are
        untouched. Return self. An empty view does nothing.

    __repr__(self):
        "Vector(" + repr(self.to_list()) + ")",
        for example "Vector([1, 2, 3])".
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

    def copy(self):
        pass

    def map(self, func):
        pass

    def __add__(self, other):
        pass

    def __radd__(self, other):
        pass

    def normalize_(self, eps=1e-5):
        pass

    def __repr__(self):
        pass
