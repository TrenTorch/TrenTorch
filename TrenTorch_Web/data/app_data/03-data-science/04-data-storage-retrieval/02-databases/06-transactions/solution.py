_DELETED = object()


class TransactionalStore:
    def __init__(self):
        self.data = {}
        self.layers = []

    def _visible(self, key):
        for layer in reversed(self.layers):
            if key in layer:
                return layer[key]
        return self.data.get(key, _DELETED) if key in self.data else _DELETED

    def set(self, key, value) -> None:
        if self.layers:
            self.layers[-1][key] = value
        else:
            self.data[key] = value

    def get(self, key):
        value = self._visible(key)
        return None if value is _DELETED else value

    def delete(self, key) -> None:
        if self.layers:
            self.layers[-1][key] = _DELETED
        else:
            self.data.pop(key, None)

    def begin(self) -> None:
        self.layers.append({})

    def commit(self) -> None:
        if not self.layers:
            raise RuntimeError("no transaction is open")
        top = self.layers.pop()
        if self.layers:
            self.layers[-1].update(top)
            return
        for key, value in top.items():
            if value is _DELETED:
                self.data.pop(key, None)
            else:
                self.data[key] = value

    def rollback(self) -> None:
        if not self.layers:
            raise RuntimeError("no transaction is open")
        self.layers.pop()

    def __len__(self) -> int:
        keys = set(self.data)
        for layer in self.layers:
            keys.update(layer)
        return sum(1 for key in keys if self.get(key) is not None)


def transfer(store: TransactionalStore, source, target, amount) -> bool:
    store.begin()
    balance = store.get(source) or 0
    if balance < amount:
        store.rollback()
        return False
    store.set(source, balance - amount)
    store.set(target, (store.get(target) or 0) + amount)
    store.commit()
    return True
