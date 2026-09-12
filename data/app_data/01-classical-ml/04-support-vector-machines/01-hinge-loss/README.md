---
name: support-vector-machines-hinge-loss
title: Hinge loss
tags: [classic-ml]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`Binary Cross-Entropy Loss` measures HOW confident a prediction is, wrong: even a correct prediction that's only slightly confident still incurs some loss, and cross-entropy keeps pushing confidence toward the extremes forever (`-log(p)` never actually reaches `0`). Support Vector Machines take a fundamentally different view of what "good enough" means: once a prediction is not just correct but correct BY A COMFORTABLE MARGIN, stop caring, that example contributes exactly zero additional loss, no matter how much MORE confident it could theoretically become.

That's hinge loss. Its whole shape is built around one number, a margin of `1`, that separates "this example is fine, ignore it" from "this example needs more attention, either wrong or too close to the boundary."

### From theory to code

Theory uses `{-1, +1}` labels (not `{0, 1}`) specifically because the formula `1 - target * scores` needs the label's SIGN to flip the score correctly for negative examples, and defines the loss as whatever's left after subtracting the margin, clipped at zero.

Implement `hinge_loss(scores, target, reduction="mean")` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `target` is `{-1, +1}`, not `{0, 1}`.
- `scores` are raw, unbounded classifier outputs, not probabilities.
- Same `reduction` modes (`"mean"`, `"sum"`, `"none"`) the other losses in this curriculum use.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`target * scores` is positive when the prediction's sign agrees with the label, and its MAGNITUDE measures how confidently correct it is.

</details>

<details>
<summary>Hint 2</summary>

`np.maximum(0.0, 1.0 - target * scores)` is the entire formula, no separate correctness check needed, the `max` with `0` handles it.

</details>

## Theory

### The simple version

A teacher grading "did the student clearly demonstrate they understood the concept" doesn't keep awarding extra credit forever as an answer gets marginally more polished, once an answer clearly, comfortably demonstrates understanding, it gets full marks, done. Cross-entropy, by contrast, is a teacher who always wants MORE confidence, an already-correct, already-confident answer can still "improve" its score infinitesimally by becoming even MORE confident. Hinge loss is the "comfortably correct, stop caring" grader: once a prediction clears a fixed bar, it contributes nothing further.

### The formula

```text
hinge_loss(scores, target) = max(0, 1 - target * scores)
```

with `target` in `{-1, +1}` (not `{0, 1}`): multiplying by a `+1` or `-1` label is what lets one formula handle both classes uniformly, for a positive example (`target = +1`), the loss is `max(0, 1 - scores)`; for a negative example (`target = -1`), it's `max(0, 1 + scores)`, exactly the mirror-image penalty.

The quantity `target * scores` is called the **margin**: positive and large means confidently, comfortably correct; positive and small (or negative) means either barely correct or outright wrong. Hinge loss is exactly zero once the margin exceeds `1`, the classifier doesn't just need to be correct, it needs to be correct with room to spare, and once it has that room, the loss stops caring how much MORE room there is. This "stop once comfortably correct" property is precisely what makes SVMs, the model family `Margin maximization intuition` (the next question) and `Linear SVM via gradient descent on hinge loss` build on this loss, focus their whole training effort on the hardest, closest-to-the-boundary examples (the "support vectors" the model family is named for) rather than continuing to over-optimize examples that are already easy.

### How PyTorch actually implements this

`torch.nn.HingeEmbeddingLoss` and `torch.nn.MultiMarginLoss` implement hinge-loss variants (the naming differs slightly across libraries, but the "margin, clipped at zero" shape is the same core idea), used less commonly in modern deep learning than cross-entropy (whose probabilistic interpretation, `08-map-estimation`'s and `02-cross-entropy`'s own connections to maximum likelihood, is often more useful for downstream tasks like calibrated confidence estimates), but still genuinely used in metric-learning and ranking losses (triplet loss, contrastive loss, both built on the same "margin" idea, seen in this curriculum's later Sequence Modeling and Vision content) where "comfortably separated" is exactly the property being optimized for, not calibrated probability.

## Explanation

`hinge_loss` computes `1.0 - target * scores` (the margin, negated and shifted), clips it at `0` via `np.maximum`, and reduces via the same `"mean"`/`"sum"`/`"none"` branching every other loss in this curriculum uses.
