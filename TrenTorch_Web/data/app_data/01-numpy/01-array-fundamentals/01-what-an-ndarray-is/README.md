---
name: numpy-what-an-ndarray-is
title: What an ndarray Is
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement a function that inspects an ndarray's memory layout facts, to build a concrete picture of how it differs from a Python list.

## Theory

A Python list doesn't store its elements directly — it stores a sequence of pointers, each pointing to a separately-allocated object elsewhere in memory. A list `[1, 2, 3]` is really three separate `int` objects, scattered in memory, with the list itself holding three addresses.

A NumPy `ndarray` is structured completely differently. It stores its actual data — not pointers — in one single, unbroken block of memory called a **buffer**, packed back-to-back with no gaps and no separate objects per element.

This has two direct consequences:

- Every element must be the same fixed size in memory, which means every element must be the same **type** (its `dtype`).
- Operations across all elements can run as a single tight loop over one memory block, rather than following a separate pointer for every element — the root reason NumPy operations are dramatically faster than an equivalent Python `for` loop over a list.

An ndarray object itself (the Python variable you interact with) is a small piece of metadata describing this buffer: where it is, what type its elements are, and what shape it should be interpreted as. The variable holding an ndarray works like any other Python variable — it stores the address of the ndarray object, which in turn describes where its data buffer lives.

## Explanation

`describe_ndarray_basics` reads `arr.dtype` and `arr.itemsize` directly off the array object rather than assuming a size from the values it happens to contain — `itemsize` is a property of the _type_ every element commits to, not of any particular value, which is exactly what makes it identical for a length-3 array and a length-3-million array of the same dtype.
