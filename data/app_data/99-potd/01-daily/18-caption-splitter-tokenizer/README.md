---
name: potd-caption-splitter-tokenizer
title: 'THE CAPTION SPLITTER'
tags: [nlp]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** NLP

---

### Story

Snap's caption-moderation pipeline needs a first-pass tokenizer before any heavier model runs.
Every unrecognized word must fall back to a single `<unk>` token, never crash the pipeline.

---

### The Math

Given a fixed vocabulary mapping word to id (id `0` reserved for `<pad>`, id `1` reserved for
`<unk>`), split the input text on whitespace and map each word to its id, using `<unk>`'s id for any
out-of-vocabulary word.

### Input Format

```
V
word_1 id_1
...
word_V id_V
caption text on one line
```

### Output Format

Space-separated token ids, one line.

### Constraints

- `1 <= V <= 10^4`, caption up to 500 characters
- Time limit: 1.0 second.

---

### Example

**Input**

```
3
the 2
cat 3
sat 4
the cat sat on mat
```

**Output**

```
2 3 4 1 1
```

## Theory

### The simple version

A tokenizer's job is to turn words into numbers a model can use, and to have a sensible fallback ready the moment it meets a word it has never seen before.

### Splitting means any whitespace run

Splitting is on any run of whitespace, matching what Python's `str.split()` (with no argument)
does, not a literal single-space split. A caption separated by a tab or by two spaces still needs to
tokenize correctly; a literal `.split(" ")` produces empty-string tokens on multiple consecutive
spaces and fails silently on tabs.

### Every out-of-vocabulary word gets the same fallback

`<unk>`'s id (always `1`, fixed by the vocabulary convention) is used for every word not in the
vocabulary, independently, word by word. A caption entirely made of unknown words is not an error,
it is a valid output of all `1`s.

### An empty caption is not an error

If the caption line is empty (or all whitespace), the output is an empty line: zero tokens, not a
crash.

## Explanation

`tokenize` builds a `word -> id` dictionary from the vocabulary once, then calls `caption.split()`
with no arguments, which splits on any run of whitespace and produces no empty strings even with
repeated separators. Each resulting word is looked up with `vocab.get(word, unk_id)`, which falls
back to the fixed `<unk>` id in one step per word without a separate membership check.
