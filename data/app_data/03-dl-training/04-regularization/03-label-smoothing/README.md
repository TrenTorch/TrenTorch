---
name: dl-training-label-smoothing
title: 'Label smoothing: softening one-hot targets before cross-entropy'
tags: [neural-networks, regularization, classification]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A standard one-hot classification target (`[1, 0, 0]` for class 0 out of 3 classes) tells cross-entropy loss to push the model toward predicting probability EXACTLY 1.0 for the correct class and EXACTLY 0.0 for every other class. But `[01-classical-ml/02-classification/10-logsoftmax-nllloss]`'s softmax can only ever approach `1.0` or `0.0` in the limit, as its raw logits grow toward `+infinity` or `-infinity`, it can never actually REACH them. A model trained against a strict one-hot target is therefore being pushed to make its logits increasingly extreme forever, which tends to make the model dangerously OVERCONFIDENT: it starts assigning probability `0.9999` to predictions that are frequently wrong, especially on inputs that are genuinely ambiguous or mislabeled, rather than reporting a more honest, moderate confidence.

Label smoothing fixes this by simply refusing to ask for a perfect `1.0`/`0.0` target in the first place: instead of `[1, 0, 0]`, the target becomes something like `[0.9333, 0.0333, 0.0333]`, still clearly favoring the correct class, but leaving a small amount of probability mass spread across every OTHER class too. The model can now actually achieve its target loss of zero without needing infinitely large logits, which empirically makes trained models noticeably better calibrated (their stated confidence more closely matches their actual accuracy) and, in many cases, modestly improves accuracy itself.

### From theory to code

Implement `smooth_labels(one_hot, smoothing, num_classes)`. Given a one-hot target vector (or a batch of them), return the smoothed version: the true class's entry becomes `1 - smoothing`, and EVERY class (including the true one) additionally gets `smoothing / num_classes` added on top.

### Constraints

- The smoothed vector for a single example must still sum to exactly `1.0` (it remains a valid probability distribution).
- With `smoothing=0`, the output must exactly equal the original one-hot input (no smoothing at all).
- Every class that was originally `0` in the one-hot vector ends up at exactly `smoothing / num_classes`, not `0`.
- The true class ends up at `(1 - smoothing) + smoothing / num_classes`, not exactly `1 - smoothing` (the small uniform amount gets added to EVERY class, the true class included).

### Hints

<details>
<summary>Hint 1</summary>

`one_hot * (1 - smoothing)` scales the original one-hot vector down (the true class becomes `1 - smoothing`, and every other class stays at `0`).

</details>

<details>
<summary>Hint 2</summary>

Add `smoothing / num_classes` to EVERY entry (not just the zero entries): `one_hot * (1 - smoothing) + smoothing / num_classes`. This uniform addition is what pushes the previously-zero classes up to a small positive value while ALSO nudging the true class's value slightly.

</details>

<details>
<summary>Hint 3: Sanity-check the sum</summary>

Sum of the smoothed vector: `sum(one_hot) * (1 - smoothing) + num_classes * (smoothing / num_classes) = 1 * (1 - smoothing) + smoothing = 1`. If your implementation doesn't sum to exactly `1`, double check you're adding `smoothing / num_classes` to every entry, not just the previously-zero ones.

</details>

## Theory

### The simple version

A teacher grading an essay question who refuses to ever award a perfect, absolute 100/100, reserving that score for genuinely impossible perfection, and instead caps the realistic best at 94/100, with the remaining few points distributed as small, honest acknowledgments across other dimensions (style, structure) even on an otherwise excellent essay. This isn't grade inflation in the other direction, it's a deliberate refusal to claim more certainty than is actually warranted, and it keeps students (or, here, a model) from chasing an unattainable, overconfident extreme.

### The formula

For a `num_classes`-length one-hot vector `y` and smoothing factor `epsilon`:

```
y_smooth[i] = y[i] * (1 - epsilon) + epsilon / num_classes    for every class i
```

Equivalently, thinking of it as a WEIGHTED AVERAGE: `y_smooth = (1 - epsilon) * one_hot_distribution + epsilon * uniform_distribution`, a mix of the original sharp one-hot target and a completely uniform distribution over all classes, controlled by `epsilon`.

### How PyTorch actually implements this

`torch.nn.CrossEntropyLoss(label_smoothing=...)` implements exactly this transformation internally (as of PyTorch 1.10+, built directly into the loss function, no separate label-preprocessing step needed), using the identical formula. Label smoothing was popularized by the original Inception-v3 paper (Szegedy et al., 2016) specifically to combat the overconfidence problem described above, and remains a standard, essentially free (adds no extra parameters, barely any extra compute) technique used across image classification and, notably, in training many modern LLMs and machine translation models, where poorly-calibrated overconfidence on ambiguous inputs is a genuine, practically-observed problem. A subtlety worth noting: label smoothing changes what the THEORETICAL MINIMUM achievable loss is, since a perfectly-predicting model that outputs the exact smoothed target distribution now has loss `> 0` (whereas an unsmoothed one-hot target has a theoretical minimum of exactly `0`), so training curves with label smoothing enabled will plateau at a visibly higher loss value than an equivalent unsmoothed run, which is expected and not itself a sign anything is wrong.

## Explanation

`smooth_labels` computes `one_hot * (1 - smoothing) + smoothing / num_classes` directly: the multiplication scales the original one-hot vector down (shrinking the true class from `1` to `1 - smoothing`, leaving every other class at `0`), and the addition then adds the SAME small constant, `smoothing / num_classes`, to every entry, including the true class. The result: the true class ends up at `(1 - smoothing) + smoothing/num_classes`, and every other class ends up at exactly `smoothing/num_classes`, with the whole vector still summing to `1.0`.
