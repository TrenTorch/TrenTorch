class Vec:
    def __init__(self, *components):
        self.data = list(components)

    def __repr__(self):
        return f"Vec({', '.join(repr(c) for c in self.data)})"

    def __eq__(self, other):
        if not isinstance(other, Vec):
            return NotImplemented
        return self.data == other.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Vec(*self.data[index])
        return self.data[index]
