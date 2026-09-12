---
name: regularized-linear-models-normal-equation
title: 'Linear Regression: closed form (Normal Equation)'
tags: [classical-ml, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Full Linear Regression Training Loop` finds the best-fit line iteratively: guess, measure the error, nudge the weights, repeat, for as many epochs as it takes to converge. For plain linear regression specifically, that iteration turns out to be unnecessary: the loss surface (`02-mse-loss`'s mean squared error, as a function of the weights) is a smooth, convex bowl with exactly one minimum, and calculus can solve for that minimum's exact location directly, in one shot, with no learning rate, no epochs, no convergence to wait for at all.

This is the Normal Equation, and understanding it matters for more than just efficiency: it's the moment where "why does gradient descent need a learning rate at all" gets a genuine answer, for THIS specific, simple problem, it doesn't, gradient descent is solving something calculus can solve exactly. Most of the models this curriculum builds (anything with a nonlinearity) don't have this luxury, which is precisely why gradient descent is the general-purpose tool used everywhere else.

### From theory to code

Theory derives the exact solution by setting the loss's gradient to zero and solving algebraically, folding the bias into the weight vector by augmenting the input with a constant column of ones.

Implement `closed_form_linear_regression(input, target)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- Return `(weight, bias)` in the exact same `(1, in_features)`/`(1,)` shapes `Full Linear Regression Training Loop` returns.
- Use `np.linalg.pinv` (the pseudoinverse), not `np.linalg.inv`, for the reason Theory explains.
- Fold the bias into the augmented system (a column of ones appended to `input`), rather than solving for it separately.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.hstack([input, np.ones((n, 1))])` appends a column of ones, turning "weight AND bias" into one single combined vector to solve for.

</details>

<details>
<summary>Hint 2</summary>

`np.linalg.pinv(X_augmented) @ target` solves the whole system in one call; the last row of the result is the bias, everything before it is the weight.

</details>

## Theory

### The simple version

Finding the lowest point of a smooth, single-valley bowl by taking tiny steps downhill (gradient descent) eventually gets you there, but if you already know calculus, you can just set the slope to zero and solve directly, no walking required, you land exactly at the bottom in one step. Linear regression's loss surface is exactly this kind of single, smooth, convex bowl, which is why an exact, one-shot formula exists for it at all.

### The formula

Augmenting `input` (shape `(n, d)`) with a column of ones gives an `(n, d+1)` matrix `X`, where the extra column lets one combined vector `theta` (shape `(d+1, 1)`) represent both the weight AND the bias at once. Setting the gradient of MSE (`03-mse-gradient`'s own gradient, `2/n * X^T @ (X @ theta - y)`) to zero and solving for `theta`:

```text
X^T @ X @ theta = X^T @ y
theta = (X^T @ X)^-1 @ X^T @ y
```

the classic Normal Equation. In practice, `(X^T X)^-1 X^T` is computed via `np.linalg.pinv(X)` (the Moore-Penrose pseudoinverse) rather than literally inverting `X^T X` and multiplying, because `X^T X` can be exactly singular or numerically ill-conditioned (`Matrix inverse, and when it does not exist`'s own warning applies directly here: if two input features are perfectly correlated, `X^T X` genuinely has no inverse), and `pinv` handles that case gracefully by finding the best least-squares solution anyway rather than crashing.

This exact-formula approach doesn't scale the way gradient descent does: solving the Normal Equation costs roughly `O(d^3)` (from the matrix inversion/pseudoinverse), which becomes prohibitively expensive once `d` (the number of features) grows into the thousands or millions, exactly the regime every deep learning model this curriculum eventually builds lives in, where gradient descent's much cheaper per-step cost (`O(d)`) is the only option.

### How PyTorch actually implements this

`torch.linalg.lstsq` computes exactly this Normal Equation solution (using a numerically stable factorization internally, similar in spirit to `pinv`), and `sklearn.linear_model.LinearRegression` uses this closed-form approach by default rather than gradient descent, precisely because plain linear regression's loss surface admits an exact answer, there's no reason to iterate when you can solve directly. The moment ANY nonlinearity enters the picture, an activation function, a neural network layer, even Ridge/Lasso regression's regularization terms (`Ridge Regression (L2)`, the next question, still has a closed form, but Lasso does not), the loss surface stops being this simple, and gradient-based optimization becomes the only generally-applicable tool, which is exactly why the rest of this curriculum builds gradient descent as the default, universal training method rather than searching for closed-form solutions everywhere.

## Explanation

`closed_form_linear_regression` augments `input` with a column of ones (folding the bias into the system), solves the augmented linear system via `np.linalg.pinv(input_augmented) @ target_col`, and splits the resulting combined vector back into `weight` (everything but the last row, transposed to `(1, in_features)`) and `bias` (the last row).
