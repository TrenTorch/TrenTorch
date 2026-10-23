---
name: sheet-asteroid-collision
title: 'Asteroid Collision'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
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

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

A collision happens only between a right-moving asteroid **on the left** and a left-moving one **on the right**. So keep a stack of asteroids that are still alive. A new right-moving one is simply pushed. A new left-moving one fights the top of the stack while the top moves right:

- if the top is **smaller**, the top explodes (pop) and the new one keeps going;
- if they are **equal**, both explode;
- if the top is **bigger**, the new asteroid explodes.

If the stack is empty or its top moves left, the new asteroid survives and is pushed. `O(n)`: each asteroid is pushed and popped at most once.

## Explanation

`alive` stays `True` while the new left-mover has not been destroyed. The while loop pops smaller right-movers; an equal one is popped with the newcomer; a bigger one stops the newcomer.
