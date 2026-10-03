---
name: python-lists-adding-removing
title: 'Adding & Removing Elements'
tags: [python-lists, mutation]
difficulty: Intermediate
---

## Statement

Implement functions that grow and shrink a list in place, demonstrating the difference between operations that mutate a list and operations that build a new one and avoiding the classic bug of removing elements while looping over the same list.

## Theory

### Adding elements: append, extend, insert

Three methods add elements to an existing list, all mutating in place and returning `None`.

| Method                 | Effect                                                          |
| ---------------------- | --------------------------------------------------------------- |
| `lst.append(x)`        | Adds **one** element, `x`, at the end.                          |
| `lst.extend(iterable)` | Adds **each element** of `iterable` at the end.                 |
| `lst.insert(i, x)`     | Inserts `x` before position `i`, shifting later elements right. |

**`append` vs `extend`.** `append` always adds exactly one element, even if that element is itself a list. `extend` unpacks its argument and adds its elements one by one:

```python
a = [1]
a.append([2, 3])       # [1, [2, 3]]      one new element: a list
b = [1]
b.extend([2, 3])       # [1, 2, 3]        two new elements
```

**`insert` and indices.** `insert` uses slice-style bounds: an index at or beyond `len(lst)` appends, and a negative index counts from the end.

**`+` and `+=`.** `lst + other` builds a **new list**; neither operand changes. `lst += other` is a **mutation**, it behaves like `lst.extend(other)` and the list keeps its address.

```python
x = [1, 2]
before = id(x)
x += [3]                 # in place: id(x) == before
x = x + [4]              # new list: id(x) != before, and x is reassigned
```

**Methods return `None`.** Because these methods mutate, they return `None`. Writing `x = x.append(3)` reassigns `x` to `None` and loses the list.

**Where this matters later.** Growing a list with `append` inside a loop and then converting it to an array is the standard way to collect per-step results (losses, predictions) in training code.

### Removing elements: remove, pop, del, clear

| Operation                      | Effect                                                                   |
| ------------------------------ | ------------------------------------------------------------------------ |
| `lst.remove(x)`                | Removes the **first** element equal to `x`. `ValueError` if none exists. |
| `lst.pop()`                    | Removes and **returns** the last element.                                |
| `lst.pop(i)`                   | Removes and returns the element at index `i`.                            |
| `del lst[i]`                   | Removes the element at index `i`.                                        |
| `del lst[a:b]`, `del lst[::k]` | Removes a whole slice.                                                   |
| `lst.clear()`                  | Removes every element; the list object stays, empty.                     |

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

`insert_sorted` scans forward with `while i < len(lst) and lst[i] <= value: i += 1`, advancing past elements _equal_ to `value`, not just less than it, which is exactly what places a new equal element after all existing ones, matching the spec's explicit "after any existing elements equal to value." `concat_identity_report` relies on `lst += extra` mutating the caller's actual list object, then `lst = lst + extra` only repointing this function's own local name afterward, the caller never sees that second reassignment, which is the point being demonstrated.

`remove_all` builds `kept = [x for x in lst if x != value]` and assigns it back via `lst[:] = kept` rather than looping and calling `.remove()` repeatedly, the "collect what to keep, then replace" pattern the theory names as the safe fix, which sidesteps the loop trap entirely instead of working around it mid-loop. `pop_last_n` clamps `n` to `len(lst)` before slicing, since a negative-index slice like `lst[-n:]` behaves incorrectly if `n` is allowed to exceed the list's own length.
