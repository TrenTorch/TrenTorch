---
name: python-sets-comprehensions-use-cases
title: 'Comprehensions & Use Cases'
tags: [python-set-comprehensions, python-set-use-cases]
difficulty: Intermediate
---

## Statement

Implement functions using set comprehensions to construct unique transformed values and filtered sets, and functions where uniqueness and repeated membership testing are central requirements, recognizing when a set is the appropriate data structure rather than using a list to simulate set behavior.

## Theory

### Set comprehensions

A **set comprehension** creates a set from an iterable using a compact expression: `{expression for variable in iterable}`, equivalent to a loop that `.add()`s each result into a fresh set.

```python
{x * 2 for x in [1, 2, 3]}          # {2, 4, 6}
```

**Uniqueness still applies**, the comprehension may evaluate its expression many times, but equal results collapse into one element: `{x % 3 for x in range(10)}` is `{0, 1, 2}`.

**Filtering with `if`** works as in list comprehensions: `{expression for variable in iterable if condition}`.

```python
{x * x for x in values if x >= 0}
```

**Multiple loops** and nested iteration work the same way as list comprehensions too.

**The expression must produce a hashable value**, since it becomes a set element, `{[x] for x in values}` raises `TypeError` because a list can't be a set element.

**Where this matters later.** Set comprehensions provide a direct way to construct unique transformed data, the same expression-and-filter structure that appears in list comprehensions.

### When a set is the right tool

A list represents an **ordered sequence**, where duplicates and position are meaningful. A set represents a **collection of unique elements**, where duplicates collapse and position doesn't exist.

| Requirement                         | Structure | Reason                           |
| ----------------------------------- | --------- | -------------------------------- |
| Preserve order/positions/duplicates | list      | Elements have sequence positions |
| Keep only unique values             | set       | Duplicates collapse              |
| Frequently test membership          | set       | Hash-based lookup is the point   |
| Access by index                     | list      | Sets have no positions           |

**Tracking seen values** is a common pattern:

```python
seen = set()
for value in values:
    if value in seen:
        ...       # already seen
    else:
        seen.add(value)
```

**Preserving first-seen order** needs both structures together, a set for membership tracking, a list for the order the result must keep:

```python
values = [3, 1, 3, 2, 1]
result = []
seen = set()
# ... -> [3, 1, 2]
```

**Where this matters later.** Sets track unique categories, vocabulary membership, or processed IDs; combining a set with a list is the standard pattern when both fast membership tracking and stable output order are required.

## Explanation

`squared_unique` squares every value inside the comprehension itself (`{x * x for x in values}`) rather than squaring first into a list and converting to a set afterward, the comprehension's own uniqueness guarantee handles duplicate squared results (e.g. `-2` and `2` both squaring to `4`) with no extra step. `positive_unique` filters with `if x > 0` _after_ the `for`, matching the spec's own boundary (`0` is excluded, since it's neither positive nor negative but the requirement is specifically "positive").

`unique_in_first_seen_order` keeps exactly the two structures the theory names side by side, a `seen` set purely for the O(1) membership check, and a `result` list purely for the order, rather than trying to make one structure do both jobs, since neither a plain list (slow membership) nor a plain set (no order) can satisfy both requirements alone. `find_duplicates` uses the same `seen`-set pattern but redirects the _second_ sighting of a value into a separate `duplicates` set instead of a list, since "which values repeated" is itself a membership question (does this value belong to the repeated group?), not an ordering question.
