class HashTable:
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key) -> list:
        return self.buckets[hash(key) % self.capacity]

    def put(self, key, value) -> None:
        bucket = self._bucket(key)
        for i, (existing, _) in enumerate(bucket):
            if existing == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self.load_factor() > 0.75:
            self._resize(self.capacity * 2)

    def _resize(self, new_capacity: int) -> None:
        pairs = [pair for bucket in self.buckets for pair in bucket]
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        for key, value in pairs:
            self._bucket(key).append((key, value))

    def get(self, key, default=None):
        for existing, value in self._bucket(key):
            if existing == key:
                return value
        return default

    def delete(self, key) -> bool:
        bucket = self._bucket(key)
        for i, (existing, _) in enumerate(bucket):
            if existing == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __len__(self) -> int:
        return self._size

    def load_factor(self) -> float:
        return self._size / self.capacity

    def keys(self) -> list:
        return [key for bucket in self.buckets for key, _ in bucket]
