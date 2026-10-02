---
name: numpy-gradient-tracking
title: 'Where Tensors Diverge: Gradient Tracking'
tags: [numpy-tensors]
difficulty: Intermediate
---

## Statement

Implement functions that model a tensor as an ndarray plus device and gradient-tracking metadata, and show how that metadata propagates through operations, is dropped by detaching, and interacts with the views/copies model.

## Theory

A tensor carries one more piece of metadata beyond shape/dtype/device: **`requires_grad`** — "record the operations involving this tensor so gradients can be computed for it."

Three rules:

1. **Propagation.** The result of an operation requires gradient tracking if _any_ input does.
2. **Detaching is a view.** A detached tensor has `requires_grad=False` but **shares the same buffer** as the original — writing through one changes the other.
3. **Moving devices is a copy.** A device transfer produces an independent buffer; if already on the requested device, the same tensor is returned.

These functions model the rules with a plain dictionary holding the ndarray and its metadata — they do not compute actual gradients.

## Explanation

`make_tensor_record` returns `{"data": data, "device": device, "requires_grad": requires_grad}` without copying `data`. `add_records` raises `ValueError` if devices differ, otherwise returns a new record with `a["data"] + b["data"]` (broadcasting applies naturally), the shared device, and `requires_grad = a["requires_grad"] or b["requires_grad"]`. `detach_record` returns a new record with `requires_grad=False` and `"data": rec["data"]` — the exact same array object, not a copy, so mutations propagate. `to_device_record` returns `rec` itself when `device == rec["device"]`, otherwise a new record with `rec["data"].copy()` on the new device.
