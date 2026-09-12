---
name: math-cross-entropy
title: "Cross-entropy, and why it's the loss Classification already uses"
tags: [information-theory]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-entropy` measured "how surprising is this distribution, to someone who already knows it exactly." Cross-entropy asks a subtly different, far more practically important question: "how surprising is the TRUE distribution, to someone whose beliefs are only an approximation of it?" That someone-with-imperfect-beliefs is exactly what a trained classifier is: it outputs a predicted probability for each class, and the true label (a one-hot distribution, all probability on the correct class) is what actually happened. Cross-entropy measures how many bits of surprise the model's imperfect beliefs cost you, on average, versus if you'd known the truth exactly.

This is not a coincidence of naming: `02-cross-entropy` (Deep Learning Core) IS this exact quantity, computed between a one-hot true label and a softmax-predicted distribution, this question builds the general concept first so that formula stops looking like an arbitrary loss and starts looking like the specific, principled thing it actually is.

### From theory to code

Theory changes exactly one thing from `01-entropy`'s formula: the log is taken of the PREDICTED distribution `q`, while the outer weighting is still by the TRUE distribution `p`. Implement that directly.

Implement `cross_entropy(p, q, base=2.0)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `p` and `q` are both valid probability distributions over the same set of outcomes.
- Clip `q` (not `p`) before taking its log, for the same `log(0)` reason `01-entropy` clips.
- `cross_entropy(p, p, base)` must equal `01-entropy`'s `entropy(p, base)` exactly, they're the same formula when `p == q`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Copy `01-entropy`'s formula and change exactly one variable name inside the `log(...)` call.

</details>

<details>
<summary>Hint 2</summary>

The outer multiplying factor stays `p` (the true weighting of outcomes), only the argument to `log` changes to `q` (the predicted probability of that outcome).

</details>

## Theory

### The simple version

Imagine you built a compression scheme optimized for a language where "e" is the most common letter (true for English). Now use that same scheme on a completely different language where letter frequencies are different. Your scheme still works, but it's no longer optimal, you'll use more bits, on average, than a scheme built specifically for that new language's true frequencies would. Cross-entropy measures exactly that gap: how many bits it costs to encode data from the TRUE distribution, using a code built for a different, PREDICTED distribution instead.

### The formula

Cross-entropy between a true distribution `p` and a predicted distribution `q`:

```text
H(p, q) = -sum_i(p_i * log_base(q_i))
```

Compare against `01-entropy`'s `H(p) = -sum_i(p_i * log_base(p_i))`, the ONLY difference is which distribution the `log` is applied to. A fundamental inequality (Gibbs' inequality) guarantees `H(p, q) >= H(p)` always, with equality exactly when `q == p`: no prediction can ever do BETTER than knowing the truth exactly, and any mismatch between predicted and true beliefs costs you extra bits, on average. This is exactly why cross-entropy makes a valid training loss: it is minimized precisely when the model's predicted distribution matches the true one, and never goes below that minimum.

When `p` is one-hot (all probability mass on a single true class, exactly what a classification label is), the formula collapses to a single term: `H(p, q) = -log(q_true_class)`, precisely `02-cross-entropy`'s (Deep Learning Core) `-log_probs[i, target[i]]` formula, this question's general two-distribution case, specialized to the one-hot label case that shows up in every classifier this curriculum trains.

### How PyTorch actually implements this

`torch.nn.functional.cross_entropy` (already implemented in `02-cross-entropy`) is precisely this formula, specialized: `p` is always one-hot (a `target` class index), so the sum in `H(p, q)` has only one nonzero term, letting the implementation skip computing a sum entirely and just index out `-log_probs[target]` directly, the exact optimization `02-cross-entropy`'s own `Explanation` describes. `torch.nn.functional.kl_div`, by contrast, computes the DIFFERENCE `H(p, q) - H(p)` directly (KL divergence, `03-kl-divergence`, the next question), used whenever the true distribution `p` is itself not one-hot, distilling a large "teacher" model's soft predictions into a smaller "student" model, for instance, where both `p` and `q` are genuine, non-degenerate probability distributions.

## Explanation

`cross_entropy` clips `q` (not `p`) away from `0` for the same `log(0)` reason `01-entropy` clips its own input, then computes `-sum(p * log(clipped_q)) / log(base)`, exactly `01-entropy`'s formula with the log's argument changed from `p` to `q`, while the outer weighting factor stays `p`.
