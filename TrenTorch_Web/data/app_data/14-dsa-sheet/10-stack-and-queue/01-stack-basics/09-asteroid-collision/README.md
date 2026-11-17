---
name: sheet-asteroid-collision
title: 'Asteroid Collision'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
theory: collisions-along-a-line
---

## Statement

Asteroids move along a line. Each number is one asteroid: its **absolute value** is its size and its **sign** is its direction (positive moves right, negative moves left). All move at the same speed.

When two asteroids meet, the **smaller one explodes**; if they have the same size, **both** explode. Asteroids moving in the same direction never meet. Return the asteroids left after all collisions, in their original order.

For `[5, 10, -5]` the answer is `[5, 10]`.

### Examples

**Example 1**

Input:

```python
asteroid_collision([5, 10, -5])
```

Output:

```text
[5, 10]
```

**Example 2**

Input:

```python
asteroid_collision([8, -8])
```

Output:

```text
[]
```

### Constraints

- `0 <= len(asteroids) <= 200000`
- `-1000 <= asteroids[i] <= 1000`, `asteroids[i] != 0`

## Explanation

`alive` stays `True` while the new left-mover has not been destroyed. The while loop pops smaller right-movers; an equal one is popped with the newcomer; a bigger one stops the newcomer.

### Complexity

- Time: O(n). Each asteroid is pushed once and popped at most once.
- Space: O(n). The stack.
