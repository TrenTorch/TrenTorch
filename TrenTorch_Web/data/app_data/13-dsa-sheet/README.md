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

### Big inputs are generated, not stored

A 10⁶-element array would be an 11 MB file. Write a generator spec instead. Every language rebuilds the
same data from the seed with the same tiny random generator (mulberry32):

```json
"nums": { "$gen": { "type": "int_array", "n": 200000, "lo": -1000, "hi": 1000, "seed": 5 } }
```

| `type`              | Fields                             | Gives                                                           |
| ------------------- | ---------------------------------- | --------------------------------------------------------------- |
| `int_array`         | `n`, `lo`, `hi`, `seed`            | `n` random ints                                                 |
| `sorted_int_array`  | same                               | the same, sorted                                                |
| `sorted_int_arrays` | `count`, `n`, `lo`, `hi`, `seed`   | `count` sorted arrays                                           |
| `permutation`       | `n`, `seed`                        | a shuffle of `0..n-1`                                           |
| `string`            | `n`, `alphabet`, `seed`            | random string                                                   |
| `cyclic_string`     | `n`, `period`, `base`              | `chr(base + i % period)`: longest all-different run is `period` |
| `int_pairs`         | `n`, `lo`, `hi`, `seed`            | `n` pairs `[a, b]` with `a <= b`                                |
| `int_matrix`        | `rows`, `cols`, `lo`, `hi`, `seed` | a matrix                                                        |
| `records`           | `n`, `names`, `lo`, `hi`, `seed`   | `n` pairs `[name, score]`                                       |

A new type needs the same code in `processes/curriculum-build/cases-runtime.py` (and later the other
languages). Keep the list short.

## What the browser receives

Only the compiled question: the README sections, `starter.py`, `solution.py`, the hints and the generated
Python tests. The tests are `processes/curriculum-build/cases-runtime.py` plus the text of `problem.json`
(`build-cases-tests.mjs`). Nothing runs on a server. The reference solution is in the page, but the IDE
shows the Solution tab only after the question is solved. The repository is public, so this is a
nudge and not a lock.

## Size limits (measured in Pyodide)

Pure-Python loops run about 2.7 times slower in Pyodide on Node and about 1.9 times slower in Chrome than in CPython 3.12. Plan with the slower number.

- About 3.7 million simple loop steps per second (Node; Chrome reached 5 million). An `O(n)` solution with `n = 2 * 10⁵` is fine; `n = 10⁶` is already about 1.5 s.
- A slow starter's first `perf` case should take 3 to 5 seconds, so it fails cleanly. The browser stops a whole run at 20 seconds.
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
