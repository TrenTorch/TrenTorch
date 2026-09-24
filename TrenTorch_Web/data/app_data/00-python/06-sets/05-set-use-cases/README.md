---
name: python-sets-use-cases
title: When a Set Solves a Problem a List Structurally Cannot
tags: [python-set-use-cases]
difficulty: Intermediate
---

## Statement

Implement functions where uniqueness and repeated membership testing are central requirements, recognizing when a set is the appropriate data structure rather than using a list to simulate set behavior.

## Theory

A list represents an **ordered sequence**, where duplicates and position are meaningful. A set represents a **collection of unique elements**, where duplicates collapse and position doesn't exist.

| Requirement | Structure | Reason |
|---|---|---|
| Preserve order/positions/duplicates | list | Elements have sequence positions |
| Keep only unique values | set | Duplicates collapse |
| Frequently test membership | set | Hash-based lookup is the point |
| Access by index | list | Sets have no positions |

**Tracking seen values** is a common pattern:

```python
seen = set()
for value in values:
    if value in seen:
        ...       # already seen
    else:
        seen.add(value)
```

**Preserving first-seen order** needs both structures together — a set for membership tracking, a list for the order the result must keep:

```python
values = [3, 1, 3, 2, 1]
result = []
seen = set()
# ... -> [3, 1, 2]
```

**Where this matters later.** Sets track unique categories, vocabulary membership, or processed IDs; combining a set with a list is the standard pattern when both fast membership tracking and stable output order are required.

## Explanation

`unique_in_first_seen_order` keeps exactly the two structures the theory names side by side — a `seen` set purely for the O(1) membership check, and a `result` list purely for the order — rather than trying to make one structure do both jobs, since neither a plain list (slow membership) nor a plain set (no order) can satisfy both requirements alone. `find_duplicates` uses the same `seen`-set pattern but redirects the *second* sighting of a value into a separate `duplicates` set instead of a list, since "which values repeated" is itself a membership question (does this value belong to the repeated group?), not an ordering question.
