class _Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.nodes = {}
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node: _Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.nodes.get(key)
        if node is None:
            return None
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key, value) -> None:
        node = self.nodes.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        node = _Node(key, value)
        self.nodes[key] = node
        self._push_front(node)
        if len(self.nodes) > self.capacity:
            oldest = self.tail.prev
            self._unlink(oldest)
            del self.nodes[oldest.key]

    def __len__(self) -> int:
        return len(self.nodes)

    def keys_by_recency(self) -> list:
        keys = []
        node = self.head.next
        while node is not self.tail:
            keys.append(node.key)
            node = node.next
        return keys
