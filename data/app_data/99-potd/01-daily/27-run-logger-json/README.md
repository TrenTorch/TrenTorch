---
name: potd-run-logger-json
title: 'THE RUN LOGGER'
tags: [mlops]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** MLOps

---

### Story

DoorDash's ML platform requires every training run, no exceptions, to log its full configuration and
final metrics before the model artifact is allowed into the registry. This is the logger every later
MLOps problem in this set assumes already exists.

---

### The Problem

No math here: this is a structured-serialization problem. Given a run id, a set of hyperparameter
key/value pairs, and a set of metric key/value pairs, produce a single canonical serialized record.

### Input Format

```
run_id
h
key_1 val_1
...
key_h val_h
m
metric_1 val_1
...
metric_m val_m
```

### Output Format

A single JSON object with keys `run_id`, `hyperparameters` (object), `metrics` (object).
Hyperparameter and metric keys are sorted alphabetically within their own object.

### Constraints

- `0 <= h, m <= 100`
- Time limit: 1.0 second.

---

### Example

**Input**

```
run_0042
2
lr 0.001
batch_size 64
1
val_loss 0.231
```

**Output**

```json
{
	"run_id": "run_0042",
	"hyperparameters": { "batch_size": "64", "lr": "0.001" },
	"metrics": { "val_loss": "0.231" }
}
```

## Theory

### The simple version

This is bookkeeping, not math: take a run's configuration and results and write them down in one consistent, predictable shape every single time, so nothing downstream has to guess at the format.

### Empty is a real value, not an omission

`h = 0` or `m = 0` means an empty object `{}` for that field, printed as `{}`, not left out of the
record entirely. A downstream consumer expecting `hyperparameters` to always be present would break
on a record that omits the key when it happens to be empty.

### The last duplicate wins

If the same hyperparameter key appears twice in the input (an upstream logging bug sending the same
value twice, or a genuine override), the later occurrence in input order overwrites the earlier one,
matching ordinary dict-overwrite semantics rather than keeping the first, or keeping both.

### Sorted keys, not insertion order

The keys inside `hyperparameters` and inside `metrics` are sorted alphabetically in the output,
independent of the order they arrived in on input. A record is still correct even when insertion
order and sorted order happen to differ.

## Explanation

`build_run_record` reads the hyperparameter pairs into a plain dict (later duplicate keys naturally
overwrite earlier ones, since each `dict[key] = value` assignment just replaces whatever was there),
does the same for the metric pairs, then returns a new dict with `run_id` and the two inner
dictionaries rebuilt with `dict(sorted(d.items()))` so their keys come out alphabetically regardless
of the input order. An empty set of pairs produces an empty dict `{}` the same way a non-empty one
does, since both just start from an empty dict and add zero or more entries to it.
