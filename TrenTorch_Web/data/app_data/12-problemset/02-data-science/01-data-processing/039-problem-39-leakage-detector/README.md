---
name: problem-39-leakage-detector
title: 'Leakage Detector'
tags: [problemset, data-stats-for-ds, data-leakage]
difficulty: Beginner
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data leakage'
hint: 'lower-case each name and test for the forbidden substrings'
tools: [NumPy]
---

## Statement

Flag feature columns whose names suggest data leakage. A column is suspicious when its lower-cased name contains any of the substrings `target`, `label`, `future`, `outcome` or `post_`.

Implement `solve(columns)`.

**Returns.** Return a list of the suspicious column names in their original order. Return an empty list when none match.

### Examples

**Example 1**

Input:

```python
solve(['age', 'income', 'target_encoded', 'future_balance', 'city'])
```

Output:

```text
['target_encoded', 'future_balance']
```

**Example 2**

Input:

```python
solve(['Age', 'Plan', 'tenure'])
```

Output:

```text
[]
```

## Theory

### The simple version

Leakage happens when a model is trained on information that would not exist at prediction time, for example a column computed from the answer itself. The model looks excellent offline and fails in production. Column names are a cheap first-pass warning sign.

### What this checks

Names containing words like _target_, _label_, _outcome_ often mean the column was derived from the answer, and names like _future_ or _post__ often mean it was recorded after the event being predicted.

## Explanation

The check is a simple substring test on the lower-cased name, so `Target_Mean` and `post_purchase_flag` are both flagged. It is a heuristic: it can flag harmless names and miss leaky columns with innocent names, so it supports a manual review rather than replacing one.
