class MinHeap:
    def __init__(self):
        self.items = []

    def push(self, x) -> None:
        self.items.append(x)
        self._sift_up(len(self.items) - 1)

    def _sift_up(self, i: int) -> None:
        items = self.items
        while i > 0:
            parent = (i - 1) // 2
            if items[i] < items[parent]:
                items[i], items[parent] = items[parent], items[i]
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        items = self.items
        n = len(items)
        while True:
            smallest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and items[child] < items[smallest]:
                    smallest = child
            if smallest == i:
                return
            items[i], items[smallest] = items[smallest], items[i]
            i = smallest

    def pop(self):
        if not self.items:
            raise IndexError("pop from an empty heap")
        smallest = self.items[0]
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            self._sift_down(0)
        return smallest

    def peek(self):
        if not self.items:
            raise IndexError("peek at an empty heap")
        return self.items[0]

    def __len__(self) -> int:
        return len(self.items)


def heapify(values: list) -> MinHeap:
    heap = MinHeap()
    heap.items = list(values)
    for i in range(len(heap.items) // 2 - 1, -1, -1):
        heap._sift_down(i)
    return heap


def top_k(stream, k: int) -> list:
    if k <= 0:
        return []
    heap = MinHeap()
    for value in stream:
        if len(heap) < k:
            heap.push(value)
        elif value > heap.peek():
            heap.pop()
            heap.push(value)
    result = []
    while len(heap):
        result.append(heap.pop())
    return result[::-1]


def merge_sorted(lists: list) -> list:
    heap = MinHeap()
    for index, values in enumerate(lists):
        if values:
            heap.push((values[0], index, 0))
    merged = []
    while len(heap):
        value, index, position = heap.pop()
        merged.append(value)
        if position + 1 < len(lists[index]):
            heap.push((lists[index][position + 1], index, position + 1))
    return merged
