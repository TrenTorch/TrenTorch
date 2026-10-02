---
name: data-storage-lru-cache
title: LRU Cache
tags: [data-structures, caching]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Memory is fast and small, disks and networks are slow and large, so systems keep recently used results close by. A cache has to decide what to throw away when it fills up, and the most common bet is that whatever was used longest ago is least likely to be needed next. That policy is **least recently used**, and the version that matters in practice does both `get` and `put` in constant time. A dictionary alone gives constant-time lookup but no sense of recency. A linked list alone gives recency but slow lookup. Combining them gives both. This question builds that combination, with the list written by hand.

### From theory to code

Implement the class `LRUCache(capacity)` with `get(key)`, `put(key, value)`, `__len__()` and `keys_by_recency()`. The skeleton and docstrings are already in the editor.

### Constraints

- `LRUCache(capacity)` holds at most `capacity` entries, with `capacity >= 1`.
- `get(key)` returns the value and marks the key as the **most recently used**. If the key is absent it returns `None` and changes nothing.
- `put(key, value)` stores the pair and marks the key as most recently used. If the key already exists its value is replaced. If adding a **new** key would exceed the capacity, the **least recently used** entry is evicted first.
- `keys_by_recency()` returns a list of all keys from most recently used to least recently used.
- Both `get` and `put` must take constant time: use a `dict` from key to node plus a **doubly linked list** of nodes that you write yourself. Do not use `collections.OrderedDict`, `functools.lru_cache`, or list operations that shift elements.

### Hints

<details>
<summary>Hint 1</summary>

Keep the list ordered by recency, with the most recent at the head. The dict gives the node for a key in constant time, and unlinking a node from a doubly linked list is constant time because it knows both neighbours.

</details>

<details>
<summary>Hint 2</summary>

Two sentinel nodes, a dummy head and a dummy tail that hold no data, remove every special case for an empty list or for the first and last node.

</details>

<details>
<summary>Hint 3</summary>

Reading a key is a use. Moving a node to the front is the same operation for `get` and for `put` on an existing key, so write it once.

</details>

## Theory

### The simple version

Think of a small desk. Whenever you use a document you put it on top of the pile. When the desk is full and a new document arrives, you shelve the one at the bottom of the pile, since it has gone untouched the longest. The pile is the linked list, and the index card telling you where each document sits in the pile is the dictionary.

### The formula

Let the cache hold at most $C$ entries. Each operation keeps one invariant: the doubly linked list is ordered from most to least recently used, and the dictionary maps each key to its node.

| Operation                  | Dictionary                  | Linked list                  | Cost   |
| -------------------------- | --------------------------- | ---------------------------- | ------ |
| `get(k)` hit               | find node                   | unlink it and insert at head | $O(1)$ |
| `get(k)` miss              | not found                   | unchanged                    | $O(1)$ |
| `put(k, v)` existing       | find node, set value        | move to head                 | $O(1)$ |
| `put(k, v)` new, room left | add key                     | insert at head               | $O(1)$ |
| `put(k, v)` new, full      | add key, delete evicted key | remove tail, insert at head  | $O(1)$ |

Unlinking a node $x$ from a doubly linked list takes four pointer updates, because $x$ knows both its neighbours:

$$
x.\text{prev}.\text{next} \leftarrow x.\text{next}, \qquad x.\text{next}.\text{prev} \leftarrow x.\text{prev}
$$

The **hit rate** is the share of lookups answered from the cache, and it is the number a cache is judged by.

### Why not a plain list

A list ordered by recency makes finding a key $O(n)$, and moving an item to the front shifts everything after it. A dictionary alone loses the order. The pair of structures is the point: each covers the weakness of the other.

### Other eviction policies

LFU evicts the least frequently used entry, FIFO the oldest, and random eviction needs no bookkeeping at all. LRU performs well when recent use predicts future use but is fooled by a one-time scan over a large dataset that flushes every useful entry. Variants such as LRU-K and ARC guard against that.

### Where this shows up

Operating-system page caches, CPU caches, database buffer pools, CDN edge caches, memoization of expensive function calls and the key-value caches of transformer inference all use LRU or close relatives.

### How NumPy/PyTorch actually implements this

`functools.lru_cache(maxsize=N)` wraps a function with an LRU cache written in C. `collections.OrderedDict` with `move_to_end` and `popitem(last=False)` is the usual short implementation. `cachetools.LRUCache` and Redis's `maxmemory-policy allkeys-lru` are production versions. PyTorch's `torch.utils.data` keeps no LRU, but decoded-sample caches in data loaders typically use one.

## Explanation

`LRUCache` keeps a dict from key to a small `_Node` holding the key, the value and `prev` and `next` pointers, and a dummy head and tail that bracket the list. `_unlink` splices a node out by pointing its two neighbours at each other, and `_push_front` inserts a node right after the head. `get` finds the node in the dict, moves it to the front and returns its value, or returns `None` for a miss. `put` updates and moves an existing node, otherwise creates a node, inserts it at the front, and if the size now exceeds the capacity removes the node just before the tail from both the list and the dict. `keys_by_recency` walks the list from the head to the tail.
