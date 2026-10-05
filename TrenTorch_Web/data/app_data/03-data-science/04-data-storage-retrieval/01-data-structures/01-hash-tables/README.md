---
name: data-storage-hash-tables
title: Hash Tables
tags: [data-structures, hashing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A Python `dict` answers "what is the value for this key?" in roughly constant time, however many entries it holds, and that speed is behind counting words, caching results, joining tables and deduplicating rows. The trick is that it does not search. It turns the key into a number, uses the number as a position in an array and looks there. Two different keys can land on the same position, and how a table handles that collision, and how it grows when it gets crowded, decides whether the constant-time promise holds. This question builds a hash table with chaining from an empty array of buckets.

### From theory to code

Implement the class `HashTable` with `put(key, value)`, `get(key, default)`, `delete(key)`, `__len__()`, `load_factor()` and `keys()`, including automatic growth when the table becomes too full. The skeleton and docstrings are already in the editor.

### Constraints

- The constructor `HashTable(capacity=8)` creates `capacity` empty buckets, and `capacity` stays readable as an attribute. Each bucket is a list of `(key, value)` pairs (**separate chaining**).
- A key goes in bucket `hash(key) % capacity`. Tests use integer keys, whose hash is the integer itself, so bucket positions are predictable.
- `put` replaces the value if the key is already present, otherwise appends a pair to the bucket and increases the size. After inserting, if `load_factor() > 0.75` the table doubles its capacity and **rehashes** every pair into the new buckets.
- `get(key, default=None)` returns the stored value or `default` when the key is absent. `delete(key)` removes the key and returns `True`, or returns `False` if it was absent. `__len__` is the number of stored keys.
- `load_factor()` returns `len(self) / capacity` as a float. `keys()` returns a list of all keys in any order.
- Do not use a `dict` or `set` to store the data. Plain lists are the only containers allowed for the buckets.

### Hints

<details>
<summary>Hint 1</summary>

A bucket is just a list. Searching it is a short linear scan, which stays short as long as the table keeps the average bucket length low.

</details>

<details>
<summary>Hint 2</summary>

When capacity doubles, a key's bucket changes because `hash(key) % capacity` now uses a different modulus. Rebuild the table from scratch by re-inserting every pair.

</details>

<details>
<summary>Hint 3</summary>

Growing happens after an insertion pushes the load factor over the limit, so check it at the end of `put`, and only when a new key was added.

</details>

## Theory

### The simple version

A coat check holds a thousand coats. Instead of searching the rack, the attendant takes your ticket number and goes straight to the hook with that number. Two tickets can map to the same hook when there are fewer hooks than possible ticket numbers, so each hook holds a short stack, and when the stacks get tall the attendant installs twice as many hooks and rehangs everything.

### The formula

A **hash function** $h$ maps a key to an integer, and the table of $m$ buckets stores the key in bucket

$$
i = h(\text{key}) \bmod m
$$

Two keys with the same $i$ **collide**. With chaining, each bucket holds a list of the colliding pairs.

The **load factor** is the average number of entries per bucket:

$$
\alpha = \frac{n}{m}
$$

With a good hash function, a lookup scans one bucket of expected length $\alpha$, so the expected cost is $O(1 + \alpha)$. Keeping $\alpha$ below a constant (here $0.75$) by **doubling** $m$ whenever it is exceeded keeps lookups constant on average.

- Doubling means each rehash costs $O(n)$, but it happens after $n/2$ cheap inserts, so the cost per insert averages out to $O(1)$ (**amortized** constant time).
- In the worst case every key lands in one bucket and a lookup degrades to $O(n)$. Real tables use well-mixed hash functions to make this vanishingly unlikely.

### Why keys must be hashable

A key's hash must never change while it is in the table, or it would be looked for in the wrong bucket. That is why Python lists cannot be dictionary keys but tuples of hashables can. Two keys that compare equal must have equal hashes, or the same key could be stored twice.

### Chaining versus open addressing

Chaining keeps colliding entries in a list per bucket, as here. **Open addressing**, used by CPython's `dict`, stores every entry directly in the array and probes other slots on a collision. It is more cache-friendly but needs tombstones for deletion and a lower load factor.

### Where this shows up in data work

Counting and grouping (`collections.Counter`, `pandas.groupby`), deduplicating rows, hash joins in databases (`02-databases/01-joins`), feature hashing in machine learning and caches all rest on this structure.

### How NumPy/PyTorch actually implements this

`dict` and `set` in CPython are open-addressing hash tables written in C, with a resize policy similar to doubling. `collections.defaultdict`, `Counter` and `OrderedDict` build on the same table. `hash()` is the built-in hash function, randomized per process for strings, which is why tests here use integer keys. `torch` has no built-in hash table but implements embedding lookups with an integer index into an array, the simplest perfect hash.

## Explanation

`HashTable` stores `capacity` lists in `self.buckets`. `put` finds the bucket with `hash(key) % capacity`, scans it for the key and replaces the value if found, otherwise appends a new pair, increments the size and checks the load factor. `_resize` allocates twice as many empty buckets, then re-inserts every pair with the new modulus so each lands in its correct new bucket, which is why growth takes one pass over the whole table. `get` and `delete` scan only the one bucket the key can live in, and `delete` removes the pair and decrements the size. `keys` concatenates the keys of all buckets.
