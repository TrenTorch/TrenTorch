---
name: classification-weighted-bce
title: 'Stretch: Class Imbalance Handling'
tags: [classical-ml, classification, class-imbalance, stretch]
difficulty: Intermediate
---

## Statement

Implement:

```python
def weighted_bce_loss(p: np.ndarray, y: np.ndarray, class_weights: dict) -> float:
    """class_weights: e.g. {0: 1.0, 1: 5.0}"""
```

## Theory

99% one-class data lets a model score deceptively low loss by always predicting the majority class.

```text
L = -mean( w_y * (y*log(p) + (1-y)*log(1-p)) )
```

## Explanation

`np.where(y == 1, class_weights[1], class_weights[0])` builds a per-sample weight array in one vectorized pass rather than looping over samples to look up each one's weight — the same vectorize-don't-loop instinct that matters far more once this runs on millions of rows than on the ten-row test cases here.
