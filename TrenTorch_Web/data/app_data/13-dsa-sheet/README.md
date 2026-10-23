# DSA Sheet: authoring guide

The sheet is a step-by-step DSA course. Each question is a folder. Tests live in a language-neutral
`problem.json` (not a `.py` file), so the same cases can later run in C++ and JavaScript. Python is
the first language and runs in the browser with Pyodide.

The sheet is not listed on `/questions`. Its questions open in the normal IDE at `/ide/<name>`.

## Folder layout

```
13-dsa-sheet/
  meta.json                              {"title": "DSA Sheet"}
  01-basics/                             a step
    meta.json
    01-counting-steps/                   a topic inside the step
      meta.json
      01-count-pairs/                    one question
        README.md                        statement, theory, explanation (same format as every other question)
        problem.json                     the contract and every test case
        starter.py                       what the student starts with
        solution.py                      reference solution (opens only after the student solves it)
        brute.py                         optional: slow but obviously correct, used by the checker only
  _tools/dsa_tool.py                     the checker (not content)
```

`README.md` follows `data/app_data/README.md`: front matter (`name`, `title`, `tags`, `difficulty`) and the
sections `## Statement`, `## Theory`, `## Explanation` in that order. Use `### Examples` and
`### Constraints` inside the Statement. The `name` starts with `sheet-` and is unique across the site.

## `problem.json`

```json
{
	"schema": 1,
	"function": {
		"name": "count_pairs",
		"params": [{ "name": "n", "type": "int" }],
		"returns": "int"
	},
	"compare": "exact",
	"limits": { "timeMs": 1000 },
	"hints": ["nudge", "key idea", "almost the answer"],
	"cases": [
		{ "id": "example_1", "visible": true, "input": { "n": 4 }, "expected": 6 },
		{ "id": "case_1", "input": { "n": 0 }, "expected": 0 },
		{
			"id": "perf_1",
			"perf": true,
			"input": { "n": 1000000000000 },
			"expected": 499999999999500000000000
		}
	],
	"stress": { "runs": 200, "inputs": { "n": { "type": "int", "lo": 0, "hi": 60 } } }
}
```

| Field           | Meaning                                                                                                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `function`      | Name, parameters (`name`, `type`) and return type of the function the student writes. Types are labels for other languages: `int`, `str`, `bool`, `list[int]`, `list[list[int]]`, ... |
| `compare`       | `exact` (default), `unordered` (same items, any order) or `float` (uses `tolerance`, default `1e-9`).                                                                                 |
| `limits.timeMs` | Time limit per case, measured in the browser (Pyodide). A case that is right but slower fails with "Time limit exceeded".                                                             |
| `hints`         | Up to four hints, shown one at a time.                                                                                                                                                |
| `cases`         | Examples first, then hidden cases, then `perf` cases. Each has an `id` (`a-z`, `0-9`, `_`), an `input` with one key per parameter, and either `expected` or `digest`.                 |
| `visible`       | The case shows its input and expected output when it fails. Hidden cases only say "Wrong answer on a hidden test case".                                                               |
| `perf`          | A big case. Once one `perf` case is too slow, the remaining `perf` cases are skipped, so a slow solution gets one clear message instead of a 20 second stop.                          |
| `digest`        | For a very large output: the first 16 hex characters of the SHA-256 of the answer's compact JSON. Use it instead of `expected`.                                                       |
| `stress`        | Checker only. Random small inputs to compare `brute.py` with `solution.py`.                                                                                                           |
| `batch`         | One case that stands for hundreds of small random cases (see below). Use it on every question.                                                                                        |
| `maxReads`      | On a case: the most values the solution may read from its list inputs (see below). Enforces O(log n) for searches.                                                                    |

### Hundreds of cases for about 1 KB: the random batch

Hand-written cases catch the bugs you thought of. A **batch** catches the ones you did not. It is one test
that runs 300 small random inputs, drawn from the question's `stress.inputs` with a seed. The file stores
only a 6-character digest of each correct answer (about 1 KB), never the inputs or the outputs:

```json
{ "id": "random_batch", "batch": { "count": 300, "seed": 1 }, "digests": ["a1b2c3", "..."] }
```

- Every run draws the same inputs, in every language (same PRNG, fields visited in alphabetical order).
- A failure shows the failing input, so the student can reproduce it.
- It only works with `compare: "exact"` and small inputs, so give `stress.inputs` ranges that stay small.
- Write it with `python data/app_data/13-dsa-sheet/_tools/dsa_tool.py batches <question-folder>`. It reads
  `solution.py`, so run it again whenever the solution or the stress ranges change.
- A batch can add `"inputs"` to use different ranges than `stress` (for example, medium sizes).
- It costs milliseconds to run and does not grow the page. Add a second batch (`random_batch_2`, another
  seed) if a question needs more.

### Enforcing O(log n): `maxReads`

You cannot time a single search: finding a value in a million-value list by scanning takes milliseconds either way.
Count the **reads** instead. A case with `"maxReads": 60` gives the solution its list inputs wrapped in a list that
counts every value read through indexing, iteration, slicing, `in`, `.index()`, `.count()`, `min()` and `sorted()`
(`bisect` works, because it reads by index). If the answer is right but the reads go over the limit, the case fails
with "too many reads" and says how many were used. Nested lists (matrices) are counted too.

```json
{
	"id": "reads_1",
	"maxReads": 60,
	"input": {
		"nums": {
			"$gen": { "type": "sorted_unique_int_array", "n": 200000, "lo": 0, "hi": 199999, "seed": 401 }
		},
		"target": 123456
	},
	"expected": 123456
}
```

Use about 3 times the reads the reference solution needs. Give the starter a plain scan with the comment
`# This is correct but reads every value`, so it fails the reads case immediately and cleanly.

### Big inputs are generated, not stored

A 10⁶-element array would be an 11 MB file. Write a generator spec instead. Every language rebuilds the
same data from the seed with the same tiny random generator (mulberry32):

```json
"nums": { "$gen": { "type": "int_array", "n": 200000, "lo": -1000, "hi": 1000, "seed": 5 } }
```

| `type`                     | Fields                                         | Gives                                                                                                   |
| -------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `int_array`                | `n`, `lo`, `hi`, `seed`                        | `n` random ints                                                                                         |
| `sorted_int_array`         | same                                           | the same, sorted                                                                                        |
| `sorted_desc_int_array`    | `n`, `lo`, `hi`, `seed`                        | the same, sorted from largest to smallest                                                               |
| `sorted_int_arrays`        | `count`, `n`, `lo`, `hi`, `seed`               | `count` sorted arrays                                                                                   |
| `permutation`              | `n`, `seed`                                    | a shuffle of `0..n-1`                                                                                   |
| `permutation_missing`      | `n`, `seed`                                    | a shuffle of `0..n` with one value left out (`n` values)                                                |
| `twice_but_one`            | `n`, `seed`                                    | the values `0..n`, one once and the rest twice, shuffled (`2n + 1` values)                              |
| `string_words`             | `n`, `alphabet`, `seed`, `max_len` (default 3) | `n` words of 1 to `max_len` letters                                                                     |
| `cyclic_words`             | `n`, `period`                                  | `["w0", "w1", ..., "w0", ...]`                                                                          |
| `sudoku_board`             | `count`, `seed`                                | a 9 by 9 board (0 = empty) with `count` random digits                                                   |
| `sorted_unique_int_array`  | `n`, `lo`, `hi`, `seed`                        | `n` different increasing values spread over `lo..hi` (`hi - lo + 1 >= n`; equal gives exactly `lo..hi`) |
| `rotated_sorted_unique`    | same                                           | that list rotated left by a random amount                                                               |
| `rotated_sorted_int_array` | `n`, `lo`, `hi`, `seed`                        | a sorted list with repeats, rotated left                                                                |
| `mountain`                 | `n`, `lo`, `hi`, `seed`                        | strictly increasing to the largest value, then strictly decreasing                                      |
| `twice_sorted_but_one`     | `n`, `lo`, `hi`, `seed`                        | sorted, every value twice except one (`2n + 1` values)                                                  |
| `sorted_grid`              | `rows`, `cols`, `k`, `seed`                    | rows and columns both strictly increasing                                                               |
| `sorted_matrix_flat`       | `rows`, `cols`, `lo`, `hi`, `seed`             | each row sorted and continuing the previous row                                                         |
| `binary_rows`              | `rows`, `cols`, `seed`                         | each row is some 0s then some 1s                                                                        |
| `balanced_parens`          | `n`, `seed`                                    | a random balanced string of `n` pairs of parentheses                                                    |
| `binary_string`            | `n`, `seed`                                    | `n` bits starting with 1                                                                                |
| `digit_string`             | `n`, `seed`                                    | `n` decimal digits with no leading zero                                                                 |
| `cyclic_string_of`         | `n`, `pattern`                                 | `pattern` repeated and cut to `n` characters                                                            |
| `roman`                    | `n`                                            | the Roman numeral for the number `n` (1 to 3999)                                                        |
| `repeat_missing`           | `n` (at least 2), `seed`                       | a shuffle of `1..n` where one value was replaced by a copy of another                                   |
| `string`                   | `n`, `alphabet`, `seed`                        | random string                                                                                           |
| `cyclic_string`            | `n`, `period`, `base`                          | `chr(base + i % period)`: longest all-different run is `period`                                         |
| `int_pairs`                | `n`, `lo`, `hi`, `seed`                        | `n` pairs `[a, b]` with `a <= b`                                                                        |
| `int_matrix`               | `rows`, `cols`, `lo`, `hi`, `seed`             | a matrix                                                                                                |
| `letter_grid`              | `rows`, `cols`, `alphabet`, `seed`             | `rows` strings of `cols` letters                                                                        |
| `edge_list`                | `n`, `lo`, `hi`, `seed`                        | `n` edges `[a, b]` between different nodes in `lo..hi`                                                  |
| `cyclic_list`              | `n`, `lo`, `hi`, `seed`                        | a `ListNode` value: `n` values and a random cycle position (`-1` to `n - 1`)                            |
| `joined_list`              | `n`, `lo`, `hi`, `param`, `size`, `seed`       | a `ListNode` value whose tail joins a random node of the list for `param` (`size` nodes) or none        |
| `repeat_but_one`           | `n`, `times`, `lo`, `hi`, `seed`               | `n + 1` different values: one once, the other `n` each `times` times, shuffled                          |
| `two_singles`              | `n`, `lo`, `hi`, `seed`                        | `n + 2` different values: two once, the other `n` twice, shuffled                                       |
| `nonzero_int_array`        | `n`, `lo`, `hi`, `seed`                        | like `int_array` but never `0`                                                                          |
| `choice_array`             | `n`, `values`, `seed`                          | `n` values picked from the list `values`                                                                |
| `int_pairs_free`           | `n`, `lo`, `hi`, `seed`                        | `n` pairs `[a, b]`, each of `a` and `b` in `lo..hi`                                                     |
| `int_pairs_pos`            | `n`, `lo`, `hi`, `seed`                        | `n` pairs `[a, b]` with `a < b`                                                                         |
| `staircase`                | `n`                                            | `n - 2, n - 3, ..., 0, 0`: every jump lands just short of the last index                                |
| `spike_array`              | `n`, `base`, `at`, `value`                     | `n` copies of `base` with `value` at index `at`                                                         |
| `jobs`                     | `n`, `max_deadline`, `max_profit`, `seed`      | `n` pairs `[deadline, profit]`                                                                          |
| `k_sorted`                 | `n`, `k`, `lo`, `hi`, `seed`                   | a sorted list where every value is at most `k` places from its place                                    |
| `stations`                 | `n`, `target`, `seed`                          | `n` gas stations `[position, fuel]` with increasing positions below `target`                            |
| `straights`                | `n`, `group`, `seed`                           | `n` groups of `group` consecutive numbers, shuffled, sometimes with one card changed                    |
| `duplicate_array`          | `n`, `seed`                                    | a shuffle of `1..n` plus one extra copy of a value                                                      |
| `car_list`                 | `n`, `step`, `lo`, `hi`, `seed`                | `n` cars `[position, speed]` with different positions                                                   |
| `rpn`                      | `n`, `seed`                                    | a valid reverse Polish expression with `n` operands that never divides by zero                          |
| `path_string`              | `n`, `seed`                                    | an absolute Unix path of `n` names, some `.` or `..`                                                    |
| `nested_encoding`          | `n`, `seed`                                    | a valid `k[text]` string with `n` top-level items                                                       |
| `stack_ops`                | `kind`, `n`, `seed`                            | valid operation lists for a stack with minimum (`min_stack`) or a queue (`queue`)                       |
| `arith_expr`               | `n`, `ops`, `hi`, `seed`                       | `n` operands joined by random operators from `ops`                                                      |
| `calc_expr`                | `n`, `hi`, `seed`                              | `n` operands with `+`, `-`, brackets and minus signs                                                    |
| `tree_level`               | `n`, `lo`, `hi`, `seed`                        | a random binary tree as a level-order list                                                              |
| `tree_level_distinct`      | `n`, `seed`                                    | the same with the values `0..n-1` shuffled                                                              |
| `symmetric_tree`           | `n`, `lo`, `hi`, `seed`                        | a root with a random tree and its mirror (sometimes one value changed)                                  |
| `skew_tree`                | `n`, `seed`                                    | a chain of `n` left children                                                                            |
| `tree_preorder`            | `n`, `seed`                                    | the preorder list of the tree with this `seed` (the values `0..n-1` shuffled)                           |
| `tree_inorder`             | `n`, `seed`                                    | the inorder list of that same tree                                                                      |
| `bst_level`                | `n`, `step`, `seed`                            | a random BST with the values `0, step, 2*step, ...`                                                     |
| `bst_or_not`               | `n`, `step`, `seed`                            | such a BST, half of the time with two values swapped                                                    |
| `bst_swapped`              | `n`, `step`, `seed`                            | such a BST with exactly two values swapped                                                              |
| `bst_preorder`             | `n`, `step`, `seed`                            | the preorder list of such a BST                                                                         |
| `skew_bst`                 | `n`, `step`                                    | a BST that is a chain of right children                                                                 |
| `skew_preorder`            | `n`, `step`                                    | the preorder list of that chain                                                                         |
| `records`                  | `n`, `names`, `lo`, `hi`, `seed`               | `n` pairs `[name, score]`                                                                               |

A new type needs the same code in `processes/curriculum-build/cases-runtime.py` (and later the other
languages). Keep the list short.

### Linked lists

A parameter of type `ListNode` is written in JSON as a list of values (`[1, 2, 3]`). The runtime builds the
nodes with the `ListNode` class from the student's own file (`starter.py` and `solution.py` define it), so
the student never writes any set-up code. A returned `ListNode` is turned back into a list of values, and
a list that loops back on itself gives a clear error.

| JSON for a `ListNode` parameter                         | Meaning                                                                                                |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `[1, 2, 3]`                                             | `1 -> 2 -> 3`                                                                                          |
| `{"values": [...], "cycle": k}`                         | the last node points back at node `k` (`-1` for no cycle)                                              |
| `{"values": [...], "join": {"param": "a", "index": k}}` | the last node points at node `k` of the list for parameter `a` (with no values, the head is that node) |
| `values` as `{"$gen": {...}}`                           | a generated list inside either object form                                                             |

A parameter of type `list[ListNode]` is a list of lists. The return type `ListNodeRef` means "a node of the
first list": the runtime turns the returned node into its position in that list (`-1` for `None`), so
"find the node where the cycle starts" is checked by identity, not by value.

### Binary trees

A parameter of type `TreeNode` is written in JSON as a **level-order list** with `null` for a missing child
(`[3, 9, 20, null, null, 15, 7]`). The runtime builds the nodes with the `TreeNode` class of the student's
file. A returned `TreeNode` is turned back into a level-order list (so a rewired tree is checked by its shape
and values), and the return type `TreeNodeVal` means "a node": the runtime compares its `val` (use it for
questions like the lowest common ancestor, with different values).

To keep the reference solutions simple, trees in the tests are at most 800 levels deep except where a question
says otherwise (Python's default recursion limit is 1000).

## What the browser receives

Only the compiled question: the README sections, `starter.py`, `solution.py`, the hints and the generated
Python tests. The tests are `processes/curriculum-build/cases-runtime.py` plus the text of `problem.json`
(`build-cases-tests.mjs`). Nothing runs on a server. The reference solution is in the page, but the IDE
shows the Solution tab only after the question is solved. The repository is public, so this is a
nudge and not a lock.

## Size limits (measured in Pyodide)

Pure-Python loops run about 2.7 times slower in Pyodide on Node and about 1.9 times slower in Chrome than in CPython 3.12. Plan with the slower number.

- About 3.7 million simple loop steps per second (Node; Chrome reached 5 million). An `O(n)` solution with `n = 2 * 10⁵` is fine; `n = 10⁶` is already about 1.5 s.
- A slow starter's first `perf` case must fail its limit **even on a fast machine**, and must not take long on a slow one. If it finishes under the limit, the next (much bigger) case runs the slow code for minutes and the browser stops the whole run at 20 seconds. Measured in Chrome, Pyodide runs 1.4 to 2.2 times slower than CPython depending on the code, and other computers differ by about 2 times either way. So keep `limits.timeMs` at **1500 or less**, make sure the reference solution takes under **half the limit** on its biggest case, and size the first big case so `starter.py` takes between **1.4 times the limit and about 3.5 seconds** on CPython. Check it with `dsa_tool.py starters`.
- Do not put a hidden "regular" case a slow starter can never finish (for example `fib(50)` for the naive recursion). Put it after the first `perf` case.
- Recursion depth of 500,000 worked in a test, with `sys.setrecursionlimit` raised.
- Keep a single list under about 10⁷ elements. A list of 32 million ints worked in Node, but a browser tab has less headroom.

## Check your question

From `TrenTorch_Web/`:

```
python data/app_data/13-dsa-sheet/_tools/dsa_tool.py check <question-folder>
python data/app_data/13-dsa-sheet/_tools/dsa_tool.py fill <question-folder>   # writes `expected` for cases that have none
npx vitest --config .config/vitest.pyodide.config.ts --run   # runs every solution in real Pyodide
```

`check` runs `solution.py` on every case and compares `brute.py` with it on random small inputs.

## Rules

- Write the statement, examples, tests and walkthrough yourself. Do not copy text from LeetCode, GeeksforGeeks, Striver's sheet or any book. A problem idea can be inspired by one; the words and test data must be new.
- Examples must have a correct expected answer from `solution.py`, never typed by hand.
- Run `ruff format` on the Python files.
