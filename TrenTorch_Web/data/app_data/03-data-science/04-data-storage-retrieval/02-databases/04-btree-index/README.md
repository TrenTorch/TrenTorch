---
name: data-storage-btree-index
title: 'B-Tree Indexes'
tags: [databases, indexes]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`02-binary-search` finds a key in a sorted array in about twenty comparisons for a million keys. On a database that is not good enough, because the keys live on disk and what costs time is not a comparison but a **page read**: fetching one block of storage. A binary search over a disk-sized array touches about twenty different blocks, each a separate read. A **B-tree** fixes this by making each node as wide as a whole page, hundreds of keys, so that the tree is only three or four levels deep and a lookup reads three or four pages. This question builds a static B-tree-style index over sorted keys, level by level, and counts the pages a search and a range scan touch.

### From theory to code

Implement `build_index(keys, fanout)`, which builds the levels of the index from sorted keys, then `search(levels, key)`, which finds a key and reports how many pages it read, then `range_scan(levels, low, high)`, which returns every key in a range and counts the pages read, then `index_height(num_keys, fanout)`, the number of levels without building the index. The signatures and docstrings are already in the editor.

### Constraints

- `keys` is a sorted list of distinct integers and `fanout >= 2` is the maximum number of entries per page.
- `build_index(keys, fanout)` returns `levels`, a list of levels from the **leaf level to the root level**. A level is a list of pages and a page is a list. The leaf level cuts `keys` into consecutive pages of up to `fanout` keys. Each higher level has one page for each group of up to `fanout` consecutive pages of the level below, holding the **smallest key of each child page**, in order. The last level has exactly one page, the root. For an empty `keys` return `[[[]]]`.
- `search(levels, key)` starts at the root page and at each non-leaf level moves to the child whose page is the last one whose first key is `<= key` (the first child if `key` is smaller than every entry). It returns `(found, pages_read)` where `found` says whether `key` is in the leaf page reached, and `pages_read` is the number of pages visited, one per level.
- `range_scan(levels, low, high)` finds the leaf page that would contain `low` as `search` does, then reads leaf pages left to right until it passes `high`. It returns `(keys_in_range, pages_read)` where `keys_in_range` is the sorted list of keys with `low <= key <= high`, and `pages_read` counts the descent from the root plus every leaf page read after the first. A range with no keys still reads the descent.
- `index_height(num_keys, fanout)` returns the number of levels `build_index` would produce, computed by repeated division (not by building the pages), as an int. For `num_keys <= fanout` (including `0`) the height is `1`.

### Hints

<details>
<summary>Hint 1</summary>

Build bottom-up. The leaf pages hold the keys. The level above holds one entry per leaf page, the smallest key in it, grouped into pages of `fanout` entries. Repeat until a single page is left.

</details>

<details>
<summary>Hint 2</summary>

Inside a non-leaf page the entries are the minimum keys of the children, so the child to follow is the last entry that is not greater than the search key. A linear scan of at most `fanout` entries is fine, since the page is already in memory.

</details>

<details>
<summary>Hint 3</summary>

Each level multiplies the number of keys reachable by `fanout`, so the height grows with the logarithm of the key count, base `fanout`.

</details>

## Theory

### The simple version

A library catalogue on paper has drawers of cards. The index on the front of the cabinet says which drawer starts at which letter, and each drawer has little dividers saying which card starts where. To find a card you read the cabinet index, open one drawer, read its dividers and take one card: three looks for a million cards, because each look narrows things down by a factor of the number of entries on that page. A B-tree is that cabinet, and the number of pages looked at is its height.

### The formula

With fanout $f$, a page holds up to $f$ entries. Level $0$ (the leaves) holds the $n$ keys in $\lceil n / f \rceil$ pages, and each higher level has $\lceil (\text{pages below}) / f \rceil$ pages, until a level has one page. The **height** is the number of levels, so

$$
h = \lceil \log_f n \rceil \quad (\text{at least } 1)
$$

and a point lookup reads exactly $h$ pages.

| Fanout $f$ | Keys $n$ | Height $h$ |
| ---------- | -------- | ---------- |
| 100        | $10^{6}$ | 3          |
| 100        | $10^{9}$ | 5          |
| 2          | $10^{6}$ | 20         |

- A binary tree is the case $f = 2$. Wide pages are what make the height tiny.
- A **range scan** pays for the descent once, then reads consecutive leaf pages. Real B+-trees link the leaves together so a scan never goes back up.
- Real B-trees also **insert** by splitting a full page in two and pushing a separator key up, keeping all leaves at the same depth. This question builds the static, read-only shape, which is what a bulk-loaded index looks like.

### Why disks & pages

Storage is read in blocks (commonly 4 to 16 kilobytes) because the cost of reaching a block dwarfs the cost of reading more of it. A node that fills a block uses that read fully, which is why B-tree fanouts are in the hundreds. The top levels are small enough to stay in memory, so a lookup in a billion-row table often costs one disk read.

### Indexes & their price

An index makes lookups and range scans on its column fast, and makes every insert, update and delete slower because the index must be changed too. A column that is searched often and updated rarely is the right candidate. A composite index on several columns serves queries on a prefix of those columns.

### How NumPy/PyTorch actually implements this

Databases such as PostgreSQL, MySQL and SQLite store their default index as a B-tree or B+-tree (`CREATE INDEX`). In Python, `sortedcontainers.SortedList` and `bisect` give sorted lookups in memory, `pandas.Index` and `.loc[low:high]` use a sorted index for slicing, and `sqlite3` is a ready-made B-tree engine in the standard library. `torch.searchsorted` does the one-level version on tensors.

## Explanation

`build_index` cuts the keys into leaf pages of up to `fanout` keys, then repeatedly builds the next level up: it takes the current level's pages in groups of `fanout`, and for each group makes a page of the first key of every page in that group, until a single page remains; the levels are returned from leaf to root. `search` descends from the root, at each non-leaf page choosing the last entry that is not greater than the key, and each step counts one page read; at the leaf it checks membership. `range_scan` descends to the leaf for `low` the same way, then reads leaf pages in order, collecting keys in the range and stopping at the first key above `high`, counting one page per leaf read. `index_height` repeats `ceil(pages / fanout)` from the number of leaf pages until it reaches one, counting levels.
