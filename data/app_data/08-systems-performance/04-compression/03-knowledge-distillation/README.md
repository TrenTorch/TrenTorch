---
name: systems-perf-knowledge-distillation
title: 'Stretch: Basic Knowledge Distillation (Reuses KL Divergence)'
tags: [mlops, neural-networks, compression]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01`/`02` shrink a model by removing weights after the fact. Knowledge distillation compresses knowledge a completely different way: train a small "student" model from scratch, but instead of only learning from the true labels, also train it to match a large, already-trained "teacher" model's _full output distribution_ — which carries far more information than a single correct-answer label ever could (a teacher's confident "70% cat, 25% dog, 5% everything else" reveals real relationships between classes that a bare label "cat" throws away entirely).

### From theory to code

Implement `distillation_loss(student_logits, teacher_logits, true_labels, temperature=2.0, alpha=0.5)`, Hinton et al.'s original distillation loss: a weighted combination of matching the teacher's temperature-softened distribution (via `03-kl-divergence`) and getting the true labels right (ordinary cross-entropy).

### Constraints

- `student_logits`, `teacher_logits`: shape `(batch_size, num_classes)`. `true_labels`: shape `(batch_size,)`, integer class indices.
- `temperature`: divides both logit sets before softmax, "softening" both distributions.
- The soft-target loss is scaled by `temperature**2` (part of the original published formula).
- `alpha` weights the soft loss; `(1 - alpha)` weights the hard-label loss. `alpha=1.0` is pure soft-target matching, `alpha=0.0` is pure ordinary cross-entropy.
- Returns a single Python `float`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Dividing logits by `temperature` before `softmax` produces a "softer" (more spread-out, less confident-looking) distribution — a higher temperature reveals more of a confident model's _relative_ confidence across every class, not just its single top prediction.

</details>

<details>
<summary>Hint 2</summary>

Compute the soft loss per sample (`kl_divergence(teacher_soft[i], student_soft[i], base=np.e)` for each row `i`), average across the batch, then multiply by `temperature**2` — this rescaling isn't optional decoration, it's part of the published formula, correcting for how dividing logits by `T` also shrinks the soft loss's own gradient magnitude by `1/T^2`.

</details>

## Theory

### The simple version

Imagine a student learning a subject not just from an answer key (which only says "correct" or "incorrect" for each question), but by watching an expert's full reasoning about _every_ possible answer — including which wrong answers the expert considered plausible and which they immediately dismissed. That richer signal, "here's my relative confidence across every option," is exactly what a teacher model's full probability distribution carries and a bare true label doesn't — and it's exactly what knowledge distillation trains the student to imitate.

### The formula

```text
student_soft = softmax(student_logits / temperature)
teacher_soft = softmax(teacher_logits / temperature)

soft_loss = mean_over_batch( KL(teacher_soft[i] || student_soft[i]) ) * temperature^2
hard_loss = cross_entropy( softmax(student_logits), true_labels )       # ordinary, T=1

distillation_loss = alpha * soft_loss + (1 - alpha) * hard_loss
```

### How PyTorch actually implements this

This is the exact loss from Hinton, Vinyals & Dean's "Distilling the Knowledge in a Neural Network" (2015), implemented in real PyTorch training code as `alpha * F.kl_div(F.log_softmax(student/T, dim=1), F.softmax(teacher/T, dim=1), reduction="batchmean") * T**2 + (1 - alpha) * F.cross_entropy(student, labels)` — verified directly in this exercise's own `tests.py`, whose `test_09_matches_real_pytorch_hinton_distillation_loss_on_a_baked_reference_case` bakes in a loss value generated once, offline, from that exact real PyTorch computation, matching this exercise's own NumPy implementation to full floating-point precision.

## Explanation

`softmax(student_logits / temperature)` and `softmax(teacher_logits / temperature)` produce the temperature-softened distributions — dividing by `temperature` before the exponential compresses the differences between logits, so `softmax` produces a less sharply-peaked (more informative about _relative_ confidence across classes) distribution.

The per-sample `kl_divergence(teacher_soft[i], student_soft[i], base=np.e)` call (reusing `03-kl-divergence` from `00-math-and-statistics/04-information-theory` directly, in natural-log units matching how distillation losses are conventionally reported) measures how far the student's softened output currently is from the teacher's — averaging across the batch and multiplying by `temperature**2` gives `soft_loss`, matching the published formula's gradient-rescaling correction.

`hard_loss` reuses `01-classical-ml/02-classification/06-softmax-cce`'s own `softmax` and `cce_loss` directly, at the _original_, unsoftened temperature — this is the ordinary supervised signal, unrelated to the teacher. The final `alpha * soft_loss + (1 - alpha) * hard_loss` blends the two according to `alpha`, exactly the weighted sum the original distillation paper proposes.
