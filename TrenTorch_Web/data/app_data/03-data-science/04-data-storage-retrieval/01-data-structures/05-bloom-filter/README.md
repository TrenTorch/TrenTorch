---
name: data-storage-bloom-filter
title: Bloom Filters
tags: [data-structures, probabilistic]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A web crawler wants to know whether it has already visited a billion URLs. A database wants to know whether a key could be in a file before it pays for a disk read. Storing every item exactly is too much memory, and an exact set is not needed when a small, controlled mistake is acceptable in one direction only. A **Bloom filter** answers "definitely not present" or "possibly present" using a handful of bits per item. It never forgets an item that was added, so it never misses, but it sometimes claims an item is present when it was never added. Those false alarms are cheap to handle, and their rate can be computed and tuned in advance. This question builds the filter and the formulas that size it.

### From theory to code

Implement the class `BloomFilter(num_bits, num_hashes)` with `add(item)` and `might_contain(item)`, then `false_positive_rate(num_items, num_bits, num_hashes)`, the expected error rate, then `optimal_num_hashes(num_bits, num_items)`, the best number of hash functions for a given size. The skeleton and docstrings are already in the editor.

### Constraints

- Items are non-negative integers, so results are the same on every run. The two base hashes are `h1 = (item * 2654435761) % 2**32` and `h2 = ((item * 40503) % 2**32) | 1`. The `i`-th bit position of an item, for `i = 0 .. num_hashes - 1`, is `(h1 + i * h2) % num_bits`.
- `BloomFilter` stores `num_bits` bits in a plain list of 0 and 1. `add(item)` sets the item's `num_hashes` bit positions to 1. `might_contain(item)` returns `True` only if every one of those positions is 1.
- An item that was added must always be reported as possibly present (**no false negatives**). `might_contain` must never modify the filter.
- `false_positive_rate(num_items, num_bits, num_hashes)` returns `(1 - exp(-num_hashes * num_items / num_bits)) ** num_hashes` as a float.
- `optimal_num_hashes(num_bits, num_items)` returns `max(1, round((num_bits / num_items) * ln 2))` as an int.

### Hints

<details>
<summary>Hint 1</summary>

Each added item switches on a few bits. Looking an item up checks whether all of its bits are on. An item never added can still find all its bits on by accident, switched on by other items, and that accident is the false positive.

</details>

<details>
<summary>Hint 2</summary>

More bits per item makes accidents rarer. More hash functions help up to a point, then they just switch on too many bits and the filter fills up.

</details>

<details>
<summary>Hint 3</summary>

`1 - exp(-k * n / m)` is the chance that a given bit is on after `n` items with `k` hashes into `m` bits. A false positive needs all `k` of an item's bits on.

</details>

## Theory

### The simple version

A nightclub bouncer has a very short guest list on a card with a hundred small boxes. For each invited guest, the bouncer ticks three boxes chosen by a fixed rule from the guest's name. A visitor is waved in only if all three of their boxes are ticked. Every invited guest gets in. A stranger gets in only if the ticks of other guests happen to cover all three of their boxes. The more guests, the more boxes are ticked and the more often a stranger slips through, but nobody on the list is ever turned away.

### The formula

After inserting $n$ items into $m$ bits using $k$ hash functions, the probability that a particular bit is still $0$ is

$$
\left(1 - \frac{1}{m}\right)^{kn} \approx e^{-kn/m}
$$

so a bit is $1$ with probability $1 - e^{-kn/m}$. A lookup for an item that was never added reports a false positive only if all $k$ of its bits are $1$:

$$
p \approx \left(1 - e^{-kn/m}\right)^{k}
$$

For fixed $m$ and $n$ this is smallest at

$$
k^{*} = \frac{m}{n}\ln 2
$$

where about half the bits are set, and the error rate is then roughly $0.6185^{m/n}$.

- Reading the formula backwards sizes the filter: for a target error $p$ and $n$ items, $m \approx -\dfrac{n \ln p}{(\ln 2)^2}$ bits. About 9.6 bits per item gives a 1% false positive rate.
- Double hashing, $g_i(x) = h_1(x) + i\,h_2(x) \bmod m$, generates all $k$ positions from two base hashes with almost no loss in quality.
- A standard Bloom filter cannot delete an item, since clearing a bit may also forget other items that share it.

### One-sided error

"Not present" is always correct and "present" is only probably correct. That asymmetry is what makes the structure useful as a **pre-filter**: ask the filter first, and only on "possibly present" pay the cost of the exact check. When most lookups are for absent items, nearly all the expensive work is avoided.

### Where this shows up

Databases (LSM-tree stores such as RocksDB and Cassandra) test a Bloom filter before reading an SSTable from disk. Web caches use them to skip one-hit wonders, browsers use them for malicious-URL checks, and data pipelines use them to deduplicate large streams and to approximate set joins.

### How NumPy/PyTorch actually implements this

No standard-library Bloom filter exists. `pybloom_live`, `bloom-filter2` and `redisbloom` provide production versions, and `numpy` boolean arrays or `bitarray` store the bits compactly. `hashlib` or `mmh3` supply stronger hash functions than the arithmetic hashes used here. Counting Bloom filters replace each bit by a small counter to allow deletion, and Cuckoo filters give deletion and better space at low error rates.

## Explanation

`BloomFilter` keeps a list of `num_bits` zeros. `_positions` computes the two base hashes from the item with the fixed constants and returns the `num_hashes` positions `(h1 + i * h2) % num_bits`, which is double hashing. `add` sets each of those positions to 1, and `might_contain` returns whether all of them are 1, never writing to the list. Because adding only ever turns bits on, every added item keeps all of its bits on forever, so there are no false negatives. `false_positive_rate` is the formula from Theory evaluated with `math.exp`, and `optimal_num_hashes` multiplies the bits per item by `ln 2` and rounds, never returning less than one.
