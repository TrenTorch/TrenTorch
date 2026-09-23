---
name: python-lists-removing-elements
title: "Removing Elements: remove, pop, del, clear"
tags: [python-lists, mutation]
difficulty: Intermediate
---

## Statement

Implement functions that delete elements from a list in place, avoiding the classic bug of removing elements while looping over the same list.

## Theory

| Operation | Effect |
|---|---|
| `lst.remove(x)` | Removes the **first** element equal to `x`. `ValueError` if none exists. |
| `lst.pop()` | Removes and **returns** the last element. |
| `lst.pop(i)` | Removes and returns the element at index `i`. |
| `del lst[i]` | Removes the element at index `i`. |
| `del lst[a:b]`, `del lst[::k]` | Removes a whole slice. |
| `lst.clear()` | Removes every element; the list object stays, empty. |

All of these mutate the list **in place**, so every variable referring to the list sees the change.

**The loop trap.** A `for` loop over a list visits positions in turn. If the loop body removes an element, everything after it shifts left, and the loop's next position skips one element:

```python
nums = [1, 1, 2]
for n in nums:
    if n == 1:
        nums.remove(n)
print(nums)        # [1, 2]   the second 1 was skipped
```

Two safe approaches: iterate over a **copy** of the list and remove from the original, or build a **new list** of the elements to keep and assign it back with slice assignment, `lst[:] = kept`, which mutates the existing object (`lst = kept` would only repoint the variable and leave the caller's list unchanged).

**Where this matters later.** Filtering data in place, and knowing whether a caller's list is modified, is a constant concern when functions receive datasets or batches as lists.

## Explanation

`remove_all` builds `kept = [x for x in lst if x != value]` and assigns it back via `lst[:] = kept` rather than looping and calling `.remove()` repeatedly — the "collect what to keep, then replace" pattern the theory names as the safe fix, which sidesteps the loop trap entirely instead of working around it mid-loop. `pop_last_n` clamps `n` to `len(lst)` before slicing, since a negative-index slice like `lst[-n:]` behaves incorrectly if `n` is allowed to exceed the list's own length.
