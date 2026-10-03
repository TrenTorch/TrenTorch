---
name: perceptron-perceptron-learning-rule
title: Perceptron learning rule
tags: [classical-ml, perceptron, linear-classifiers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The perceptron is the simplest learning neuron: it fires (outputs 1) when a weighted sum of its inputs passes zero, and it learns by nudging its weights only when it gets a sample wrong.

### From theory to code

Implement `perceptron_train(X, y, lr=1.0, epochs=100)`. Sweep the samples in order each epoch; whenever the prediction `1 if w @ x + b > 0 else 0` is wrong, move the weights and bias towards the correct answer. Stop early after an epoch with no mistakes.

### Constraints

- `X` has shape `(n_samples, n_features)`; `y` holds labels in `{0, 1}`.
- Start from `w = 0` and `b = 0.0`; process samples in the given order, updating immediately after each mistake.
- Return `(w, b)` where `w` is a float array and `b` a Python float.
- Do not modify `X` or `y`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The error for a sample is `y - prediction`, which is `0` (correct), `+1` (should have fired) or `-1` (should not have).

</details>

<details><summary>Hint 2</summary>

The update is `w += lr * error * x` and `b += lr * error`; a correct sample has error 0 and changes nothing.

</details>

## Theory

### The simple version

Whenever the neuron is wrong, tilt the decision line a little towards the misclassified point. If the classes can be separated by a straight line, this is guaranteed to stop after finitely many mistakes. If they cannot (XOR), it never settles.

### The formula

$$\hat{y} = \mathbb{1}\big[w^{\top}x + b > 0\big]$$

$$w \leftarrow w + \eta\,(y - \hat{y})\,x, \qquad b \leftarrow b + \eta\,(y - \hat{y})$$

### How libraries implement this

scikit-learn ships `sklearn.linear_model.Perceptron`; deep-learning frameworks treat the same unit as a `Linear` layer followed by a step function (which has no useful gradient, hence the sigmoid in later models).

## Explanation

Updating inside the inner loop is what makes this the classic online perceptron. Breaking when an epoch has zero mistakes is exactly the convergence condition for separable data.
