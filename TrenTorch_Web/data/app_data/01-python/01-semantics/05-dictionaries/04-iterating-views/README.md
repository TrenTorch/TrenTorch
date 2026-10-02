---
name: python-dicts-iterating-views
title: 'Iterating: keys(), values(), items()'
tags: [python-dicts, iteration]
difficulty: Intermediate
---

## Statement

Implement functions that traverse dictionaries correctly, including modifying a dictionary during traversal without triggering an error.

## Theory

**Three views.** `d.keys()` yields each key, `d.values()` each value, `d.items()` each `(key, value)` pair. A plain `for key in d` visits the keys, same as `d.keys()`. To visit pairs, unpack in the loop header: `for key, value in d.items(): ...`.

**These return views, not copies.** A view refers to the dictionary itself and reflects later changes to it. `list(d)`, `list(d.values())`, `list(d.items())` build a real, independent snapshot from a view.

**Changing a dictionary during iteration.** Changing the _value_ of an existing key is fine inside a loop. Adding or removing keys during a loop over the same dictionary raises `RuntimeError: dictionary changed size during iteration`. To add or remove keys while looping, iterate over a **snapshot**:

```python
for key in list(d):            # the list is a separate object
    if d[key] < 0:
        del d[key]             # safe: the loop is over the list, not over d
```

**Sorted traversal.** `sorted(d)` sorts the keys. `sorted(d.items())` sorts `(key, value)` tuples by key (tuples compare element by element). To order by value instead, use a key function that returns the second element of each pair.

**Membership on views.** `key in d` and `key in d.keys()` are both fast (hash lookup); `value in d.values()` scans every value.

**Where this matters later.** Iterating `named_parameters()` and `state_dict().items()` in PyTorch uses exactly `for key, value in ...items()`.

## Explanation

`remove_where_value_below` loops over `list(d.items())` — a real snapshot list, not the live `items()` view — specifically so deleting keys mid-loop never touches the object actually being iterated, avoiding the "changed size during iteration" error the theory calls out. `items_by_value_desc` runs `sorted(d.items())` first (ascending by key, since tuples compare element by element) and _then_ `sorted(..., key=value_of, reverse=True)`, relying on the second sort's stability to keep the first sort's key-ascending order among value ties — exactly the two-stable-sorts technique from the Lists module's ordering topic, applied here to dictionary entries.
