---
name: math-gradient-descent
title: 'Gradient Descent as an Optimization Loop'
tags: [calculus]
difficulty: Intermediate
widget: gradient-descent-playground
---

## Statement

### The problem, from first principles

`06-directional-derivatives` establishes that the gradient points in the direction of steepest **ascent** — but it stops there, never actually using that fact to find a minimum. Gradient descent is the direct, obvious consequence: if the gradient points toward the steepest increase, walking a small step in the **opposite** direction decreases the function, and repeating that over and over eventually reaches a minimum. This question implements the loop itself, not just the formula.

### From theory to code

Implement `gradient_descent_step(x, gradient_fn, learning_rate)`, performing a single update, then `gradient_descent(x0, gradient_fn, learning_rate, num_steps)`, running the full loop and returning every intermediate position. The signatures and docstrings are already in the editor.

### Constraints

- `x` may be a scalar float or a NumPy array (the same update rule applies elementwise either way).
- `gradient_fn` takes `x` and returns the gradient at that point, same shape as `x`.
- `gradient_descent` returns a list of length `num_steps + 1`: the starting point `x0`, followed by the position after each of the `num_steps` updates.

### Hints

<details>
<summary>Hint 1</summary>

`gradient_descent_step` is one line: `x - learning_rate * gradient_fn(x)` — the entire "walk downhill" idea, applied once.

</details>

<details>
<summary>Hint 2</summary>

`gradient_descent` just calls `gradient_descent_step` in a loop, appending each new position to a running list that starts with `x0` already in it.

</details>

## Theory

### The simple version

Standing on a hillside in fog, unable to see the valley but able to feel which way is steepest underfoot, the obvious strategy is: take a small step in the downhill direction, feel the slope again, take another small step, and repeat — eventually you reach a low point. Gradient descent is exactly this strategy, made precise: "feel the slope" is computing the gradient, and "small step downhill" is subtracting a small multiple of that gradient from the current position.

### The formula

$$
x_{t+1} = x_t - \eta \, \nabla f(x_t)
$$

- `x_t` — the current position at iteration `t`.
- `∇f(x_t)` — the gradient of `f` at `x_t` (`06-directional-derivatives`), pointing toward steepest **ascent**.
- `η` (eta) — the **learning rate**, a small positive number controlling how big a step to take; too small and progress is slow, too large and the step can overshoot the minimum entirely (`07-taylor-series`'s Theory explains exactly why: the update trusts a first-order, straight-line approximation of `f`, which stops being accurate once the step is large enough to reach a region of different curvature).
- Subtracting (rather than adding) the gradient is precisely what turns "steepest ascent direction" into "steepest **descent** direction" — negating a direction always reverses it.

### Try it live

<div class="tt-widget" data-widget="gradient-descent-playground">
	<canvas id="gdcanvas"></canvas>
	<div class="controls">
		<div class="ctrl">
			<label>Learning rate (η) <b id="lrVal">0.10</b></label>
			<input type="range" id="lrSlider" min="0.01" max="0.5" step="0.01" value="0.1" />
		</div>
		<div class="btnrow">
			<button class="wbtn" id="stepBtn" type="button">Step</button>
			<button class="wbtn primary" id="playBtn" type="button">Play</button>
		</div>
		<button class="wbtn" id="resetBtn" type="button">Reset</button>
		<div class="readout">
			<div>Position <b id="roPosition">—</b></div>
			<div>Loss <b id="roLoss">—</b></div>
			<div>Gradient <b id="roGradient">—</b></div>
			<div>Iteration <b id="roIteration">0</b></div>
		</div>
	</div>
</div>

The curve has a few bumps deliberately, so a learning rate that's too large visibly overshoots or oscillates rather than smoothly descending — try dragging the learning rate up while playing and watch the red dot's trail (amber) start to zig-zag instead of settling.

### Why this doesn't always find the true minimum

Gradient descent only ever follows the **local** slope — on a bumpy function with multiple valleys (exactly the curve in the widget above), it can settle into a nearby dip that isn't the deepest one available, simply because it never looks anywhere the local gradient doesn't point. This is the core limitation `05-numerical-computation`'s "Gradient-based optimization: convexity, critical points, and saddle points" question examines directly, using the Hessian (`05-hessian`) to distinguish a genuine minimum from a saddle point the gradient alone can't tell apart (the gradient is exactly zero at both).

### How PyTorch actually implements this

`torch.optim.SGD` implements exactly this update rule (`param -= lr * param.grad`) as its core step, with everything else PyTorch's optimizers add (momentum, Adam's adaptive per-parameter learning rates) built as refinements on top of this same basic loop, not a replacement for it — every optimizer in the Deep Learning Training track's `optimizers` questions is, underneath, this exact idea with extra bookkeeping.

## Explanation

`gradient_descent_step` returns `x - learning_rate * gradient_fn(x)`, a direct one-line translation of the update formula — works identically whether `x` is a scalar or a NumPy array, since both support elementwise subtraction and scalar multiplication the same way. `gradient_descent` initializes a list with `x0`, then loops `num_steps` times, each iteration calling `gradient_descent_step` on the current last element and appending the result — returning the full trajectory (not just the final point) is what lets the widget above draw every intermediate position as a visible trail.
