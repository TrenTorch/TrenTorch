---
name: data-storage-transactions
title: Transactions
tags: [databases, transactions]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Moving 100 from one bank account to another is two writes: subtract here, add there. If the machine fails between them, 100 has vanished. A **transaction** groups writes so that they take effect together or not at all, and that all-or-nothing promise, the A in ACID, is what lets people trust a database. It also lets a program try something and undo it. The classic way to understand transactions is to build a small in-memory key-value store with `begin`, `commit` and `rollback`, where transactions can be nested and a rollback throws away only the innermost one. This question builds that store and uses it for a safe transfer.

### From theory to code

Implement the class `TransactionalStore` with `set`, `get`, `delete`, `begin`, `commit`, `rollback` and `__len__`, then `transfer(store, source, target, amount)`, which moves money atomically. The skeleton and docstrings are already in the editor.

### Constraints

- `set(key, value)` stores a value and `get(key)` returns it, or `None` if the key is absent or deleted. `delete(key)` removes a key (a missing key is not an error). `__len__` is the number of keys currently visible.
- `begin()` opens a new transaction level. Transactions can be **nested** to any depth. Writes made inside a transaction are visible to reads in that transaction and in transactions opened inside it (**read your own writes**), but they are not permanent.
- `commit()` makes the innermost transaction's writes part of its parent: the next level out, or the permanent store if it was the outermost. `rollback()` discards the innermost transaction's writes and leaves everything else as it was. Both raise `RuntimeError` if no transaction is open.
- A `delete` inside a transaction hides the key from reads in that transaction, and is itself undone by `rollback`.
- `transfer(store, source, target, amount)` moves `amount` from the integer balance at `source` to the one at `target` inside its own transaction. If `source` has less than `amount` (a missing balance counts as `0`), it rolls back and returns `False` without changing anything. Otherwise it commits and returns `True`.
- Use plain dicts. Do not copy the entire store when a transaction begins: keep only the changes made at each level.

### Hints

<details>
<summary>Hint 1</summary>

Keep a stack of change-sets, one per open transaction. A change-set maps a key to its new value, or to a marker meaning "deleted".

</details>

<details>
<summary>Hint 2</summary>

To read a key, look in the innermost change-set first, then the next one out and finally in the permanent data. The first place that mentions the key decides the answer.

</details>

<details>
<summary>Hint 3</summary>

Committing a level merges its change-set into the one below it (or into the permanent data), and rolling it back just drops it.

</details>

## Theory

### The simple version

Writing a letter on a pad, you can scribble a draft on a separate sheet laid over the page. If you like it, you copy it onto the page. If you do not, you throw the sheet away and the page is untouched. Nested transactions are a stack of such sheets: each sheet shows your changes on top of the sheets below it, accepting a sheet pastes its contents onto the sheet beneath, and discarding it removes only the top one.

### The formula

A database that supports transactions promises four properties, **ACID**:

| Property        | Promise                                                            |
| --------------- | ------------------------------------------------------------------ |
| **A**tomicity   | all of a transaction's writes happen, or none do                   |
| **C**onsistency | a transaction takes the data from one valid state to another       |
| **I**solation   | concurrent transactions do not see each other's half-finished work |
| **D**urability  | once committed, a change survives a crash                          |

The store built here shows atomicity directly. If $L_0$ is the permanent data and $L_1, \dots, L_d$ are the change-sets of the open transactions (innermost last), a read of key $k$ returns the value from the **innermost** level that mentions $k$:

$$
\text{get}(k) = L_j[k] \quad \text{where } j = \max\{\, i : k \in L_i \,\}
$$

- `commit` on level $d$ replaces $L_{d-1}$ by $L_{d-1}$ overridden with $L_d$, and removes level $d$. `rollback` removes level $d$ unchanged.
- Cost: reads cost $O(d)$ and a commit costs $O(\text{size of the change-set})$. Nothing is copied when a transaction starts.
- A deletion is recorded as a special marker in a change-set, because "absent from this level" must be told apart from "deleted at this level".

### Isolation & durability

This store has one user, so isolation is not tested. Real databases let many transactions run at once and offer isolation levels, from read committed to serializable, trading speed for protection against anomalies such as dirty and non-repeatable reads. Durability comes from a **write-ahead log**: the intent of a transaction is written to disk before the change is applied, so after a crash the log can be replayed.

### Where this shows up

Every SQL database exposes `BEGIN`, `COMMIT` and `ROLLBACK`, with `SAVEPOINT` for the nested form built here. Python's `sqlite3` connection is a transaction context manager, and the same stack-of-changes idea appears in software transactional memory, undo systems in editors and the copy-on-write layers of container filesystems.

### How NumPy/PyTorch actually implements this

`sqlite3.connect(...)` in the standard library gives real ACID transactions (`with conn:` commits or rolls back), and `SAVEPOINT name` / `ROLLBACK TO name` give nesting. PostgreSQL, MySQL and every other relational database implement the same commands. `collections.ChainMap` is a stack of dicts where a read searches from the innermost map outward, exactly the lookup rule used here.

## Explanation

`TransactionalStore` keeps the permanent data in one dict and a list of change-set dicts, one per open transaction. A deleted key is stored in a change-set as a private marker object. `get` searches the change-sets from the innermost outward and then the permanent data, returning `None` when the first level that mentions the key holds the marker. `set` and `delete` write into the innermost change-set, or straight into the permanent data when no transaction is open. `commit` pops the innermost change-set and applies it to the level below, applying deletion markers as deletions at the permanent level or keeping them as markers in a parent change-set. `rollback` just pops it. `__len__` counts keys whose visible value is not `None`. `transfer` opens a transaction, checks the source balance through `get`, and either rolls back or applies both writes and commits.
