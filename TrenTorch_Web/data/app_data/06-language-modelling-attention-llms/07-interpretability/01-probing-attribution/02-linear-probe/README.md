---
name: lm-linear-probe
title: Linear Probes
tags: [interpretability, probing, logistic-regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Does a model's hidden state _contain_ some property, say whether a sentence is in the past tense or whether a number is even? A **linear probe** answers by training the simplest possible classifier, a logistic regression, on frozen activations. If a linear map can read the property off the hidden state, the model represents it in an easily accessible way. A probe is only as informative as it is simple: a powerful probe could learn the property itself rather than read it, so interpretability work keeps probes linear and compares against a control. You will build the probe from scratch with gradient descent and an L2 penalty.

### From theory to code

Implement `train_linear_probe` and `probe_accuracy`.

### Constraints

- `X` has shape `(n, d)` and `y` holds 0/1 labels. The probe is `p = sigmoid(X @ w + b)`.
- `train_linear_probe(X, y, steps, lr, l2)` starts from `w = 0` and `b = 0` and performs `steps` full-batch gradient-descent updates on the mean cross-entropy plus `0.5 * l2 * ||w||^2` (the bias is not penalized). Return `(w, b)`.
- The gradient of the data term is `X.T @ (p - y) / n` for `w` and `mean(p - y)` for `b`. The penalty adds `l2 * w` to the weight gradient.
- `probe_accuracy(X, y, w, b)` is the fraction of examples where `(X @ w + b > 0)` equals `y`.
- Use a stable sigmoid.

### Hints

<details>
<summary>Hint 1</summary>

The sigmoid of a large negative number overflows `exp`; use `0.5 * (1 + np.tanh(z / 2))`.

</details>

<details>
<summary>Hint 2</summary>

Writing the gradient with the residual `p - y` is the same expression you used for the bigram network.

</details>

## Theory

### The simple version

To test whether a document folder is already sorted by topic, you hand an intern one simple rule (a straight line in some measurement space). If even that rule separates the topics, the sorting was already there.

### The formula

$$
\mathcal{L}(w, b) = -\frac{1}{n}\sum_i \big[y_i \ln p_i + (1-y_i)\ln(1-p_i)\big] + \frac{\lambda}{2}\lVert w\rVert^2, \quad p_i = \sigma(w^\top x_i + b)
$$

$$
\nabla_w \mathcal{L} = \tfrac{1}{n} X^\top (p - y) + \lambda w, \qquad \nabla_b \mathcal{L} = \tfrac{1}{n}\sum_i (p_i - y_i)
$$

### How this is done in practice

Probing papers use scikit-learn's `LogisticRegression` on cached activations from a chosen layer and token position, and report accuracy against a baseline such as probing a randomly initialized model. Variants include the _difference of means_ direction used for steering and _control tasks_ that estimate how much a probe can memorize.

## Explanation

Training is plain gradient descent on a convex objective, so it converges to the global optimum for small enough `lr`. The L2 term keeps the weights bounded on perfectly separable data, where the unpenalized solution runs off to infinity.
