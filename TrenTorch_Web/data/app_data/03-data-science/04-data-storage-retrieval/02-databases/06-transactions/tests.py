"""
pytest tests.py
"""

import pytest

from _load import load_solution

_module = load_solution(__file__)
TransactionalStore = _module.TransactionalStore
transfer = _module.transfer


# ---- 1-4: without transactions ----


def test_1_set_get_delete():
    store = TransactionalStore()
    store.set("a", 1)
    assert store.get("a") == 1
    store.delete("a")
    assert store.get("a") is None


def test_2_missing_key_is_none_and_deleting_it_is_fine():
    store = TransactionalStore()
    assert store.get("x") is None
    store.delete("x")


def test_3_len_counts_visible_keys():
    store = TransactionalStore()
    store.set("a", 1)
    store.set("b", 2)
    store.delete("a")
    assert len(store) == 1


def test_4_commit_and_rollback_without_a_transaction_raise_runtime_error():
    store = TransactionalStore()
    with pytest.raises(RuntimeError):
        store.commit()
    with pytest.raises(RuntimeError):
        store.rollback()


# ---- 5-10: one transaction ----


def test_5_writes_in_a_transaction_are_visible_to_reads_in_it():
    store = TransactionalStore()
    store.begin()
    store.set("a", 1)
    assert store.get("a") == 1


def test_6_rollback_discards_the_writes():
    store = TransactionalStore()
    store.set("a", 1)
    store.begin()
    store.set("a", 2)
    store.set("b", 3)
    store.rollback()
    assert store.get("a") == 1 and store.get("b") is None and len(store) == 1


def test_7_commit_makes_the_writes_permanent():
    store = TransactionalStore()
    store.begin()
    store.set("a", 5)
    store.commit()
    assert store.get("a") == 5
    with pytest.raises(RuntimeError):
        store.rollback()


def test_8_delete_inside_a_transaction_hides_the_key_and_rollback_restores_it():
    store = TransactionalStore()
    store.set("a", 1)
    store.begin()
    store.delete("a")
    assert store.get("a") is None and len(store) == 0
    store.rollback()
    assert store.get("a") == 1


def test_9_committed_delete_removes_the_key_for_good():
    store = TransactionalStore()
    store.set("a", 1)
    store.begin()
    store.delete("a")
    store.commit()
    assert store.get("a") is None and len(store) == 0


def test_10_overwriting_and_reading_back_inside_the_transaction():
    store = TransactionalStore()
    store.set("a", 1)
    store.begin()
    store.set("a", 2)
    store.set("a", 3)
    assert store.get("a") == 3
    store.rollback()
    assert store.get("a") == 1


# ---- 11-16: nesting ----


def test_11_inner_rollback_leaves_the_outer_transaction_intact():
    store = TransactionalStore()
    store.begin()
    store.set("a", 1)
    store.begin()
    store.set("a", 2)
    store.set("b", 9)
    store.rollback()
    assert store.get("a") == 1 and store.get("b") is None
    store.commit()
    assert store.get("a") == 1


def test_12_inner_commit_goes_to_the_parent_and_can_still_be_rolled_back_with_it():
    store = TransactionalStore()
    store.begin()
    store.begin()
    store.set("a", 7)
    store.commit()  # into the outer transaction
    assert store.get("a") == 7
    store.rollback()  # the outer transaction is discarded
    assert store.get("a") is None


def test_13_inner_transaction_sees_the_outer_writes():
    store = TransactionalStore()
    store.begin()
    store.set("a", 1)
    store.begin()
    assert store.get("a") == 1
    store.set("a", 2)
    assert store.get("a") == 2
    store.rollback()
    assert store.get("a") == 1


def test_14_inner_delete_committed_to_the_parent_then_committed_permanently():
    store = TransactionalStore()
    store.set("a", 1)
    store.begin()
    store.begin()
    store.delete("a")
    store.commit()
    assert store.get("a") is None
    store.commit()
    assert store.get("a") is None and len(store) == 0


def test_15_three_levels_deep():
    store = TransactionalStore()
    store.set("x", 0)
    for level in (1, 2, 3):
        store.begin()
        store.set("x", level)
    assert store.get("x") == 3
    store.rollback()
    assert store.get("x") == 2
    store.rollback()
    assert store.get("x") == 1
    store.commit()
    assert store.get("x") == 1


def test_16_beginning_a_transaction_does_not_copy_the_store():
    store = TransactionalStore()
    for i in range(1000):
        store.set(i, i)
    store.begin()
    assert store.layers[-1] == {}


# ---- 17-20: atomic transfer ----


def test_17_transfer_moves_the_money():
    store = TransactionalStore()
    store.set("alice", 100)
    store.set("bob", 20)
    assert transfer(store, "alice", "bob", 30) is True
    assert store.get("alice") == 70 and store.get("bob") == 50


def test_18_insufficient_funds_changes_nothing():
    store = TransactionalStore()
    store.set("alice", 10)
    store.set("bob", 0)
    assert transfer(store, "alice", "bob", 50) is False
    assert store.get("alice") == 10 and store.get("bob") == 0


def test_19_missing_target_account_is_created_and_missing_source_counts_as_zero():
    store = TransactionalStore()
    store.set("alice", 10)
    assert transfer(store, "alice", "carol", 4) is True
    assert store.get("carol") == 4
    assert transfer(store, "nobody", "alice", 1) is False


def test_20_total_money_is_conserved_over_many_transfers():
    store = TransactionalStore()
    for name, balance in (("a", 50), ("b", 50), ("c", 50)):
        store.set(name, balance)
    for source, target, amount in [("a", "b", 30), ("b", "c", 90), ("c", "a", 25), ("a", "c", 500)]:
        transfer(store, source, target, amount)
    assert sum(store.get(name) for name in ("a", "b", "c")) == 150
