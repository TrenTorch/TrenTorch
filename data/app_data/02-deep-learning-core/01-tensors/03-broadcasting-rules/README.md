---
name: dl-core-broadcasting-rules
title: Broadcasting rules
tags: [deep-learning, tensors]
difficulty: Intermediate
---

## Statement

Implement:

```python
def broadcast_shapes(shape_a, shape_b) -> tuple[int, ...] | None:
    """Returns the broadcast result shape, or None if incompatible."""
```

## Theory

`02-elementwise-ops`'s functions all quietly relied on broadcasting to handle a scalar against an array, or two differently-shaped arrays, without ever stating the rule that makes that legal. Broadcasting is precisely defined, not "NumPy figures it out somehow": align the two shapes' dimensions starting from the _right_ (the trailing/last dimensions), padding the shorter shape with `1`s on the left as needed, then compare each aligned pair of dimensions. Two dimensions are compatible if they're equal, or if either one is exactly `1` (a size-`1` dimension "stretches" to match the other), and the result dimension is whichever of the two is larger.

```text
shape_a = (8, 1, 6, 1)
shape_b =    (7, 1, 5)     # padded to (1, 7, 1, 5) to align lengths
             ↓ compare each aligned pair
result  = (8, 7, 6, 5)
```

This is exactly the rule `01-hypothesis-function`'s Theory alluded to when warning about a `(batch_size, 1)` prediction silently broadcasting against a `(batch_size,)` target, that specific footgun is this exact rule applying somewhere the shapes happened to be compatible but not actually what the caller meant. Understanding the precise rule is what lets you predict _when_ broadcasting will silently "work" (and possibly compute the wrong thing) versus when it will correctly raise an error.

## Explanation

`broadcast_shapes` pads whichever shape is shorter with `1`s on the _left_ (`(1,) * len_diff + tuple(shorter_shape)`), this is what "align from the right" means concretely, the trailing dimensions of both shapes end up compared against each other regardless of how many leading dimensions either shape originally had.

Then it walks the two (now equal-length) shapes pairwise with `zip`, checking `dim_a == dim_b or dim_a == 1 or dim_b == 1` for each pair, exactly the compatibility rule Theory states, and appending `max(dim_a, dim_b)` to the result whenever a pair passes. The moment any pair fails that check, the function returns `None` immediately, there's no way to "partially" broadcast two shapes, one incompatible dimension pair makes the whole operation invalid.
