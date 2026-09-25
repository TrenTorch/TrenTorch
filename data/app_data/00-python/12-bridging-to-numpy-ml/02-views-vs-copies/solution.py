class View:
    def __init__(self, buffer, indices=None):
        self.buffer = buffer
        self.indices = indices if indices is not None else range(len(buffer))

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return View(self.buffer, self.indices[key])
        return self.buffer[self.indices[key]]

    def __setitem__(self, key, value):
        self.buffer[self.indices[key]] = value

    def to_list(self):
        return [self.buffer[i] for i in self.indices]


def shares_buffer(a, b) -> bool:
    return a.buffer is b.buffer


def scale_in_place(view, k) -> None:
    for i in range(len(view)):
        view[i] = view[i] * k


def scaled_copy(view, k) -> list:
    return [x * k for x in view.to_list()]
