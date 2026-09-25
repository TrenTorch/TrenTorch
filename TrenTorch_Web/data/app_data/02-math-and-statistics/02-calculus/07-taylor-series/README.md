---
name: math-taylor-series
title: 'Taylor Series Expansion, and Why Gradient Descent Is a First-Order Approximation'
tags: [calculus]
difficulty: Intermediate
widget: taylor-approximation
---

## Statement

### The problem, from first principles

`05-hessian` computes a function's curvature at a point, but never connects that number to what it's actually _for_: predicting the function's value nearby without re-evaluating it. Taylor series is that connection — a way to approximate any smooth function, near a chosen point, using only its derivatives at that one point. It also explains, precisely, why gradient descent (`08-gradient-descent`) only ever needs the gradient: gradient descent is quietly using just the **first-order** Taylor approximation and discarding everything else.

### From theory to code

Implement `taylor_first_order(f, f_prime, a, x)`, the tangent-line approximation of `f` at `x`, centered at `a`, then `taylor_second_order(f, f_prime, f_double_prime, a, x)`, adding the next term. The signatures and docstrings are already in the editor.

### Constraints

- `f`, `f_prime`, `f_double_prime` are functions taking a single float and returning a float.
- `a` is the expansion point; `x` is where the approximation is evaluated (may equal `a`, or be arbitrarily far from it — accuracy degrades with distance, but the formula itself is defined everywhere).
- Both approximations must equal `f(a)` exactly when `x == a`.

### Hints

<details>
<summary>Hint 1</summary>

The first-order term is exactly `05-hessian`'s tangent-plane idea in one dimension: `f(a) + f'(a) * (x - a)` — the function's value at `a`, plus a linear correction based on the slope there.

</details>

<details>
<summary>Hint 2</summary>

The second-order term adds `(f''(a) / 2) * (x - a)²` — note the `/ 2`, which comes directly from the general Taylor series formula's `n!` denominator (`03-factorial-and-binomial-coefficient`) at `n = 2`.

</details>

## Theory

### The simple version

If you know a road's exact elevation and slope at one point, you can predict the elevation a short distance away reasonably well by just following that slope in a straight line — that's the first-order approximation. If you also know how sharply the slope itself is changing (curvature), you can do better by predicting a gently curving path instead of a straight one — that's the second-order approximation. Keep adding terms (third-order, fourth-order, ...) and the approximation matches the true function over an increasingly wide range, in exchange for needing increasingly many derivatives.

### The formula

$$
f(x) \approx \sum_{n=0}^{N} \frac{f^{(n)}(a)}{n!} (x - a)^n
$$

- `f^{(n)}(a)` — the `n`-th derivative of `f`, evaluated at the expansion point `a` (`f^{(0)}(a) = f(a)` itself, `f^{(1)}(a) = f'(a)`, and so on).
- `n!` — `03-factorial-and-binomial-coefficient`'s factorial, appearing as a normalizing denominator that comes directly out of repeatedly differentiating and re-integrating the series (a full derivation belongs to a calculus course, not this question, but the factorial's presence is not arbitrary).
- `Σ_{n=0}^{N}` (`01-summation-notation`) — summing terms up to some chosen order `N`; `N=1` gives the first-order (tangent-line) approximation, `N=2` gives second-order, and so on.
- Truncating the sum at any finite `N` is itself an approximation — the true function equals the **infinite** sum (for a function that has a convergent Taylor series at all), and every term left out is exactly the approximation's error.

### Try it live

<div class="tt-widget" data-widget="taylor-approximation">
	<canvas id="tacanvas"></canvas>
	<div class="controls">
		<div class="ctrl">
			<label>Expansion point (a) <b id="aVal">0.0</b></label>
			<input type="range" id="aSlider" min="-3" max="3" step="0.1" value="0" />
		</div>
		<div class="readout">
			<div>a <b id="roA">0.00</b></div>
			<div>1st-order error at a+2 <b id="roError1">—</b></div>
			<div>2nd-order error at a+2 <b id="roError2">—</b></div>
		</div>
	</div>
</div>

Grey is the true `sin(x)`; red is the 1st-order (tangent-line) approximation; amber is the 2nd-order approximation. Drag `a` and watch both approximations hug the true curve closely near the green dot, then diverge further away — the 2nd-order curve always tracks a little longer before diverging, since it captures one more derivative's worth of information.

### Why gradient descent is exactly the first-order case

Gradient descent's entire update rule, `x_{new} = x - \eta \nabla f(x)`, is a direct consequence of minimizing the first-order Taylor approximation of `f` near the current point `x`, subject to a small step-size constraint — it never looks at curvature at all (that would require the Hessian, `05-hessian`, and is exactly what distinguishes it from second-order methods like Newton's method, which use the Hessian to take a smarter, curvature-aware step). This is why gradient descent's steps can overshoot or zig-zag on a function with high curvature relative to the chosen learning rate `η` — the linear approximation it's implicitly trusting stops being accurate exactly where curvature is strong, which the method has no way of detecting on its own.

### How PyTorch actually implements this

Nothing in PyTorch computes a Taylor series explicitly for ordinary training — but `torch.autograd.functional.hessian` exists specifically for the cases (certain optimization diagnostics, some second-order optimizers) where a second-order approximation's extra accuracy is worth its much higher computational cost, exactly the trade-off this question's Theory describes abstractly.

## Explanation

`taylor_first_order` returns `f(a) + f_prime(a) * (x - a)` — the tangent line's value at `x`, guaranteed to equal `f(a)` when `x == a` since the second term vanishes. `taylor_second_order` returns the same first-order expression plus `(f_double_prime(a) / 2) * (x - a) ** 2`, the next term in the general formula at `n = 2`, using the `/ 2!` (which equals `/ 2`) factor directly from Theory's summation formula.
