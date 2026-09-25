---
name: python-strings-text-vs-bytes
title: Text vs Bytes
tags: [python-strings, encoding]
difficulty: Intermediate
---

## Statement

Implement functions that convert between text and bytes, measuring how many bytes a string needs and verifying round trips.

## Theory

A `str` is a sequence of **characters** (code points). Computers store and transmit **bytes**: integers from `0` to `255`. An **encoding** maps each character to one or more bytes; **decoding** is the reverse.

```python
data = "Hi".encode("utf-8")     # b'Hi'
data[0]                         # 72       an int, not a string
list(data)                      # [72, 105]
data.decode("utf-8")            # "Hi"
```

**UTF-8** uses a variable number of bytes per character:

| Code point range        | Bytes per character |
| ----------------------- | ------------------- |
| U+0000 – U+007F (ASCII) | 1                   |
| U+0080 – U+07FF         | 2                   |
| U+0800 – U+FFFF         | 3                   |
| U+10000 and above       | 4                   |

The important consequence: **`len(s)` counts characters, while `len(s.encode("utf-8"))` counts bytes**, and the two are equal only when every character is ASCII.

Decoding bytes with the wrong encoding, or bytes not valid in the chosen encoding, produces `UnicodeDecodeError`. Both `encode` and `decode` accept an `errors` argument: `"strict"` (default, raises), `"replace"` (substitutes a placeholder), and `"ignore"` (drops the offending data).

```python
"café".encode("ascii", errors="ignore")      # b'caf'
```

**Where this matters later.** Byte-level tokenizers used by language models start from exactly this representation: text is encoded to UTF-8, and each resulting integer is a basic token before larger tokens are learned.

## Explanation

`is_ascii_only` compares `len(s)` against `len(s.encode("utf-8"))` rather than looping over characters checking `ord(ch) < 128` — the theory's own consequence ("the two lengths are equal only when every character is ASCII") is a direct, O(1)-per-character test that needs no explicit per-character branch. `roundtrip` passes `errors="replace"` only on the encode step; by the time decoding runs, the bytes already came from a successful (possibly lossy) encode of that same encoding, so they're guaranteed valid to decode without needing `errors="replace"` again.
