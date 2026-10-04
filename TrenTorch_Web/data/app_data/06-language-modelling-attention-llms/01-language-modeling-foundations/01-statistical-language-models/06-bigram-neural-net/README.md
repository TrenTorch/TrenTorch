---
name: lm-bigram-neural-net
title: Bigram Neural Network
tags: [language-modeling, neural-networks, gradient-descent]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The count table and a tiny neural network can represent the same model. Give every symbol a one-hot vector, multiply by a weight matrix `W` of shape `(V, V)` to get **logits** (unnormalized log-probabilities), and apply softmax to turn each row into a distribution. Multiplying a one-hot vector by `W` just selects a row, so row `i` of `W` plays the role of the logits for "what follows symbol `i`". The difference is how you obtain the numbers: instead of counting, you start with `W = 0` (a uniform model) and nudge it by gradient descent to lower the NLL of the training pairs. This is the first step from statistics to learning: the same loss, the same softmax and the same update rule scale up unchanged to transformers.

### From theory to code

Implement `bigram_net_loss`, `bigram_net_gradient` and `train_bigram_net` for training pairs `(xs[k], ys[k])` meaning symbol `ys[k]` followed symbol `xs[k]`.

### Constraints

- `xs` and `ys` are integer arrays of the same length and `W` has shape `(V, V)`. Row `xs[k]` of `W` holds the logits for pair `k`.
- `bigram_net_loss(W, xs, ys)` is the mean over pairs of `-log softmax(W[xs[k]])[ys[k]]`. Use a numerically stable softmax by subtracting the row maximum.
- `bigram_net_gradient(W, xs, ys)` is the exact gradient of that mean loss with respect to `W`: for each pair add `softmax(W[x]) - onehot(y)` to row `x`, then divide by the number of pairs.
- `train_bigram_net(xs, ys, V, steps, lr)` starts from `W = zeros((V, V))` and applies `steps` plain gradient-descent updates `W -= lr * gradient`. Return `W`.

### Hints

<details>
<summary>Hint 1</summary>

Let `P = softmax(W[xs])` have shape `(n, V)`. Subtract 1 at the true column of each row, then scatter-add the rows into a `(V, V)` array indexed by `xs` with `np.add.at`.

</details>

<details>
<summary>Hint 2</summary>

`np.add.at(grad, xs, P)` accumulates correctly even when the same row index repeats, which `grad[xs] += P` does not.

</details>

## Theory

### The simple version

It is the same table as before, but learned instead of counted. Every pair that appears pushes up the logit of the symbol that followed and pushes down the logits of the others, in proportion to how wrong the current prediction was. Pairs the model already predicts well barely move it.

### The formula

For one pair with $p = \text{softmax}(z)$, $z = W_x$:

$$
\mathcal{L} = -\ln p_y, \qquad \frac{\partial \mathcal{L}}{\partial z_k} = p_k - \mathbf{1}[k = y]
$$

Averaging over $n$ pairs and routing each pair's gradient to its row $x$ gives $\nabla_W \mathcal{L} = \frac{1}{n}\sum_k e_{x_k}\,(p^{(k)} - e_{y_k})^\top$. At the optimum each row of $\text{softmax}(W)$ equals the empirical frequencies, which are the maximum-likelihood counts from the previous questions.

### How this is done in practice

In PyTorch this is `nn.Embedding(V, V)` followed by `F.cross_entropy`, with `loss.backward()` computing the gradient you derive here by hand and `torch.optim.SGD` applying the update. Choosing `W` of shape `(V, V)` is special to the bigram case. For longer contexts the embedding is shrunk to a small dimension and followed by further layers, which is exactly what the next questions in this track build.

## Explanation

The gradient function evaluates a stable softmax for each training pair, subtracts the one-hot target and accumulates into the row of the input symbol. Training repeats that for a fixed number of steps. Rows that never occur as inputs receive no gradient and stay uniform, which is the correct "I have no evidence" answer. Rows that do occur converge towards the empirical next-symbol frequencies, so the learned network and the count table agree, only the route to the answer differs.
