class TransactionalStore:
    """
    An in-memory key-value store with nested transactions. Keep only the
    changes made at each level; do not copy the whole store on begin().
    """

    def __init__(self):
        """Starts empty with no transaction open."""
        # TODO: Create the permanent data and the stack of change-sets.
        pass

    def set(self, key, value) -> None:
        """Stores key -> value in the innermost open transaction (or permanently)."""
        # TODO: Write into the innermost change-set.
        pass

    def get(self, key):
        """
        Returns the visible value: the innermost level that mentions the
        key decides. None if the key is absent or deleted.
        """
        # TODO: Search the change-sets from the innermost outward.
        pass

    def delete(self, key) -> None:
        """Hides the key. A missing key is not an error. Undone by rollback."""
        # TODO: Record a deletion marker in the innermost change-set.
        pass

    def begin(self) -> None:
        """Opens a new, possibly nested, transaction."""
        # TODO: Push an empty change-set.
        pass

    def commit(self) -> None:
        """
        Merges the innermost transaction into its parent (or into the
        permanent data). Raises RuntimeError if none is open.
        """
        # TODO: Apply the innermost change-set one level down.
        pass

    def rollback(self) -> None:
        """Discards the innermost transaction. Raises RuntimeError if none is open."""
        # TODO: Drop the innermost change-set.
        pass

    def __len__(self) -> int:
        """Returns the number of keys currently visible."""
        # TODO: Count the keys whose visible value is not None.
        pass


def transfer(store: TransactionalStore, source, target, amount) -> bool:
    """
    Inside one transaction, moves `amount` from the integer balance at
    `source` to `target`. If source has less than amount (a missing
    balance is 0), rolls back and returns False with nothing changed.
    Otherwise commits and returns True.
    """
    # TODO: Use begin, commit and rollback so both writes happen or neither.
    pass
