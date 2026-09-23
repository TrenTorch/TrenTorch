---
name: potd-torque-minimizer-gd-step
title: 'THE TORQUE MINIMIZER'
tags: [calculus, optimization]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Calculus, Optimization

---

### Story

An Amazon warehouse robot arm's joint controller minimizes a quadratic torque-penalty cost function
before every movement, cheap enough to run at control-loop frequency, but it still needs a correct
gradient step, not an approximation.

---

### The Math

```
C(theta) = a * theta^2 + b * theta + c
dC/dtheta = 2*a*theta + b
```

Given `a, b, c` and a starting `theta_0`, take one gradient-descent step with learning rate `eta`:

```
theta_1 = theta_0 - eta * dC/dtheta at theta_0
```

### Input Format

```
a b c theta_0 eta
```

### Output Format

`theta_1` and `C(theta_1)`, space-separated, to 6 decimal places.

### Constraints

- `-100 <= a, b, c, theta_0 <= 100`, `a != 0`, `0 < eta <= 1`
- Time limit: 1.0 second.

---

### Example

**Input**

```
1.0 -4.0 5.0 0.0 0.1
```

**Output**

```
0.400000 3.560000
```

**Explanation:** `dC/dtheta` at `0` is `-4.0`, so `theta_1 = 0 - 0.1 * (-4.0) = 0.4`, and
`C(0.4) = 1(0.16) - 4(0.4) + 5 = 3.56`.

## Theory

### The simple version

The gradient at a point tells you which way is uphill and how steep it is. One step of gradient descent walks a little bit downhill from wherever you currently are, using that slope.

### One step, not a loop

This is a single deterministic arithmetic computation: substitute `theta_0` into the gradient
formula, then take one step. No iteration, no convergence check, and no symbolic differentiation
library is needed or expected.

### Negative `a` is still just one step

If `a` is negative the cost is concave and this step moves away from any stationary point, but the
task is only to report the mechanical result of one gradient step, not to detect or correct for
divergence.

### Already at the vertex

At `theta_0 = -b / (2a)` the gradient is exactly `0`, so `theta_1 = theta_0`: the step changes
nothing, which is the correct behavior, not a special case to branch on.

## Explanation

`gd_step` computes `grad = 2 * a * theta_0 + b` directly from the closed-form derivative, takes
`theta_1 = theta_0 - eta * grad`, and evaluates `C(theta_1) = a * theta_1**2 + b * theta_1 + c` by
direct substitution. Every operation is exact floating-point arithmetic with no iteration, so a very
small `eta` or a `theta_0` already at the vertex both fall out of the same formula without a branch.
