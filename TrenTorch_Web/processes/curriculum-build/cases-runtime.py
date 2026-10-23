import copy
import hashlib
import json
import sys
import time

# Runtime for DSA questions whose tests live in problem.json. buildTestHarness
# (processes/ide-content/build-test-harness.ts) puts this text in front of the generated test file, and data/app_data/13-dsa-sheet/_tools/dsa_tool.py
# imports it to check the reference solution, so both run the same code.
#
# Inputs are plain JSON. A large input is not stored: it is a {"$gen": {...}} spec that every
# language can rebuild from a seed with the same tiny PRNG (mulberry32), so C++ and JS later get
# the identical arrays.


# Set when a performance case runs over its limit: the remaining performance cases are skipped, so
# a slow solution gets one clear "Time limit exceeded" and not a 20 second hard stop.
STATE = {"slow": False}


def _mulberry32(seed):
    state = [seed & 0xFFFFFFFF]

    def next_u32():
        state[0] = (state[0] + 0x6D2B79F5) & 0xFFFFFFFF
        t = state[0]
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return (t ^ (t >> 14)) & 0xFFFFFFFF

    return next_u32


def _shuffle(items, rnd):
    for i in range(len(items) - 1, 0, -1):
        j = rnd() % (i + 1)
        items[i], items[j] = items[j], items[i]
    return items


def _gen(spec):
    rnd = _mulberry32(spec.get("seed", 1))
    kind = spec["type"]
    n = spec.get("n", 0)
    lo, hi = spec.get("lo", 0), spec.get("hi", 0)
    if kind == "int_array":
        return [lo + rnd() % (hi - lo + 1) for _ in range(n)]
    if kind == "sorted_int_array":
        return sorted(lo + rnd() % (hi - lo + 1) for _ in range(n))
    if kind == "sorted_desc_int_array":
        return sorted((lo + rnd() % (hi - lo + 1) for _ in range(n)), reverse=True)
    if kind == "string":
        alphabet = spec["alphabet"]
        return "".join(alphabet[rnd() % len(alphabet)] for _ in range(n))
    if kind == "permutation":
        # a shuffle of 0..n-1 (Fisher-Yates driven by the portable PRNG)
        return _shuffle(list(range(n)), rnd)
    if kind == "permutation_missing":
        # a shuffle of 0..n with one random value left out (n values)
        items = list(range(n + 1))
        items.pop(rnd() % (n + 1))
        return _shuffle(items, rnd)
    if kind == "twice_but_one":
        # n + 1 different values 0..n: one appears once, the other n appear twice (2n + 1 values)
        values = _shuffle(list(range(n + 1)), rnd)
        return _shuffle(values + values[1:], rnd)
    if kind == "repeat_missing":
        # a shuffle of 1..n where one value was overwritten by a copy of another (needs n >= 2)
        items = _shuffle(list(range(1, n + 1)), rnd)
        i = rnd() % n
        j = rnd() % n
        if i == j:
            j = (j + 1) % n
        items[i] = items[j]
        return items
    if kind == "int_matrix":
        return [
            [lo + rnd() % (hi - lo + 1) for _ in range(spec["cols"])]
            for _ in range(spec["rows"])
        ]
    if kind == "string_words":
        # n words, each 1..max_len letters from `alphabet` (max_len defaults to 3)
        alphabet = spec["alphabet"]
        max_len = spec.get("max_len", 3)
        words = []
        for _ in range(n):
            length = 1 + rnd() % max_len
            words.append(
                "".join(alphabet[rnd() % len(alphabet)] for _ in range(length))
            )
        return words
    if kind == "cyclic_words":
        # ["w0", "w1", ..., "w<period-1>", "w0", ...] with n words
        return ["w" + str(i % spec["period"]) for i in range(n)]
    if kind == "sudoku_board":
        # a 9x9 board (0 = empty) with `count` random digits 1..9 at random cells
        cells = _shuffle(list(range(81)), rnd)
        board = [[0] * 9 for _ in range(9)]
        for cell in cells[: spec["count"]]:
            board[cell // 9][cell % 9] = 1 + rnd() % 9
        return board
    if (
        kind in ("sorted_unique_int_array", "rotated_sorted_unique", "mountain")
        and n == 0
    ):
        return []
    if kind == "rotated_sorted_int_array":
        # a sorted_int_array (repeats allowed) rotated left by a random amount
        items = sorted(lo + rnd() % (hi - lo + 1) for _ in range(n))
        if n == 0:
            return items
        k = rnd() % n
        return items[k:] + items[:k]
    if kind == "sorted_matrix_flat":
        # rows x cols whose values increase along each row and continue in the next row
        total = spec["rows"] * spec["cols"]
        step = (hi - lo + 1) // total
        flat = [lo + i * step + rnd() % step for i in range(total)]
        return [
            flat[r * spec["cols"] : (r + 1) * spec["cols"]] for r in range(spec["rows"])
        ]
    if kind == "binary_rows":
        # each row: some 0s then some 1s (the number of 0s is random from 0 to cols)
        rows = []
        for _ in range(spec["rows"]):
            zeros = rnd() % (spec["cols"] + 1)
            rows.append([0] * zeros + [1] * (spec["cols"] - zeros))
        return rows
    if kind == "sorted_unique_int_array":
        # n different values, increasing, spread over lo..hi (hi - lo + 1 >= n; equal means lo..hi)
        step = (hi - lo + 1) // n
        return [lo + i * step + rnd() % step for i in range(n)]
    if kind == "rotated_sorted_unique":
        # a sorted_unique_int_array rotated left by a random amount
        step = (hi - lo + 1) // n
        items = [lo + i * step + rnd() % step for i in range(n)]
        k = rnd() % n
        return items[k:] + items[:k]
    if kind == "mountain":
        # strictly increasing up to the largest value, then strictly decreasing (n values)
        step = (hi - lo + 1) // n
        items = [lo + i * step + rnd() % step for i in range(n)]
        top = items.pop()
        left, right = [], []
        for value in items:
            (left if rnd() % 2 == 0 else right).append(value)
        return left + [top] + right[::-1]
    if kind == "twice_sorted_but_one":
        # a sorted list where every value appears twice except one (2n + 1 values)
        values = [lo + i * ((hi - lo + 1) // (n + 1)) for i in range(n + 1)]
        single = rnd() % (n + 1)
        out = []
        for i, value in enumerate(values):
            out.extend([value] if i == single else [value, value])
        return out
    if kind == "sorted_grid":
        # rows x cols, strictly increasing along every row and every column
        k = spec.get("k", 1000)
        return [
            [(i + j) * k + rnd() % k for j in range(spec["cols"])]
            for i in range(spec["rows"])
        ]
    if kind == "balanced_parens":
        # a random balanced string of n pairs of parentheses (2n characters)
        out = []
        opens = closes = 0
        for _ in range(2 * n):
            if opens < n and (closes >= opens or rnd() % 2 == 0):
                out.append("(")
                opens += 1
            else:
                out.append(")")
                closes += 1
        return "".join(out)
    if kind == "binary_string":
        # n bits starting with 1 (a single bit may be 0)
        if n == 0:
            return ""
        bits = ["1" if n > 1 else str(rnd() % 2)]
        bits.extend(str(rnd() % 2) for _ in range(n - 1))
        return "".join(bits)
    if kind == "cyclic_string_of":
        # `pattern` repeated and cut to n characters
        pattern = spec["pattern"]
        return (pattern * (n // len(pattern) + 1))[:n]
    if kind == "roman":
        # the Roman numeral for the number n (1..3999)
        out = []
        for value, symbol in (
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ):
            while n >= value:
                out.append(symbol)
                n -= value
        return "".join(out)
    if kind == "digit_string":
        # n decimal digits with no leading zero (a single digit may be 0)
        if n == 0:
            return ""
        first = 1 + rnd() % 9 if n > 1 else rnd() % 10
        return str(first) + "".join(str(rnd() % 10) for _ in range(n - 1))
    if kind == "cyclic_string":
        # s[i] is chr(base + i % period): n characters with the longest all-different run = period
        return "".join(chr(spec.get("base", 97) + i % spec["period"]) for i in range(n))
    if kind == "int_pairs":
        # n pairs [a, b] with lo <= a <= b <= hi
        pairs = []
        for _ in range(n):
            a = lo + rnd() % (hi - lo + 1)
            b = lo + rnd() % (hi - lo + 1)
            pairs.append([min(a, b), max(a, b)])
        return pairs
    if kind == "letter_grid":
        # `rows` strings of `cols` letters from `alphabet`
        alphabet = spec["alphabet"]
        return [
            "".join(alphabet[rnd() % len(alphabet)] for _ in range(spec["cols"]))
            for _ in range(spec["rows"])
        ]
    if kind == "edge_list":
        # n edges [a, b] between different nodes in lo..hi (needs hi > lo)
        edges = []
        for _ in range(n):
            a = lo + rnd() % (hi - lo + 1)
            b = lo + rnd() % (hi - lo)
            edges.append([a, b + 1 if b >= a else b])
        return edges
    if kind == "sorted_int_arrays":
        # `count` sorted arrays of `n` ints each
        return [
            sorted(lo + rnd() % (hi - lo + 1) for _ in range(n))
            for _ in range(spec["count"])
        ]
    if kind == "records":
        # n [name, score] records: names from `names`, score in [lo, hi]
        names = spec["names"]
        return [
            [names[rnd() % len(names)], lo + rnd() % (hi - lo + 1)] for _ in range(n)
        ]
    raise ValueError("unknown generator: " + kind)


def sample_input(spec, rnd):
    """One random value for a stress/batch spec: an int, a choice, or a generator whose size
    fields may be {min, max}. Fields are visited in alphabetical order so every language that
    uses the same PRNG draws the same numbers."""
    kind = spec["type"]
    if kind == "int":
        return spec["lo"] + rnd() % (spec["hi"] - spec["lo"] + 1)
    if kind == "choice":
        return spec["values"][rnd() % len(spec["values"])]
    gen = dict(spec)
    for key in sorted(spec):
        value = spec[key]
        if isinstance(value, dict) and set(value) == {"min", "max"}:
            gen[key] = value["min"] + rnd() % (value["max"] - value["min"] + 1)
    gen["seed"] = rnd()
    return _gen(gen)


def batch_args(problem, batch, index):
    """The arguments of random case `index` (0-based) in a batch: the same on every run."""
    inputs = batch.get("inputs") or problem["stress"]["inputs"]
    rnd = _mulberry32((batch["seed"] * 100003 + index) & 0xFFFFFFFF)
    order = [p["name"] for p in problem["function"]["params"]]
    return {name: sample_input(inputs[name], rnd) for name in order}


class _Reads:
    def __init__(self):
        self.count = 0


class _CountedList(list):
    """A list that counts how many values the code reads from it, for cases with maxReads.
    Reading by index, iterating, slicing, `in`, `.index` and `.count` all count."""

    def __init__(self, items, reads):
        super().__init__(items)
        self._reads = reads

    def __getitem__(self, index):
        if isinstance(index, slice):
            self._reads.count += len(range(*index.indices(len(self))))
        else:
            self._reads.count += 1
        return list.__getitem__(self, index)

    def __iter__(self):
        for value in list.__iter__(self):
            self._reads.count += 1
            yield value

    def __reversed__(self):
        for value in list.__reversed__(self):
            self._reads.count += 1
            yield value

    def __contains__(self, value):
        self._reads.count += len(self)
        return list.__contains__(self, value)

    def index(self, *args):
        self._reads.count += len(self)
        return list.index(self, *args)

    def count(self, value):
        self._reads.count += len(self)
        return list.count(self, value)


def _counted(value, reads):
    if not isinstance(value, list):
        return value
    if value and isinstance(value[0], list):
        value = [_counted(row, reads) for row in value]
    return _CountedList(value, reads)


def _materialize(value):
    if isinstance(value, dict) and "$gen" in value:
        return _gen(value["$gen"])
    return copy.deepcopy(value)


def _without_digit_limit(call):
    # Python 3.11+ refuses to turn an int with more than 4300 digits into text, or text into
    # one. Answers like fibonacci(50000) are bigger, so lift the limit just for this call.
    old = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)
    try:
        return call()
    finally:
        sys.set_int_max_str_digits(old)


def _dumps(x, **kwargs):
    return _without_digit_limit(lambda: json.dumps(x, **kwargs))


def _canon(x):
    return _without_digit_limit(lambda: json.loads(json.dumps(x)))


def _digest(x):
    return hashlib.sha256(
        _dumps(_canon(x), separators=(",", ":")).encode()
    ).hexdigest()[:16]


def _short(x, limit=160):
    text = _dumps(_canon(x))
    return (
        text
        if len(text) <= limit
        else text[:limit] + "... (" + str(len(text)) + " chars)"
    )


def _same(actual, expected, compare, tolerance):
    actual, expected = _canon(actual), _canon(expected)
    if compare == "float":
        if isinstance(expected, list):
            return len(actual) == len(expected) and all(
                abs(a - e) <= tolerance for a, e in zip(actual, expected)
            )
        return abs(actual - expected) <= tolerance
    if compare == "unordered":

        def key(v):
            return _dumps(v, sort_keys=True)

        return sorted(actual, key=key) == sorted(expected, key=key)
    return actual == expected


def _check_batch(problem, case, fn):
    """Many small seeded random cases in one test. Each answer is checked against a short digest
    stored in the file, so hundreds of cases cost about 1 KB."""
    batch = case["batch"]
    order = [p["name"] for p in problem["function"]["params"]]
    limit_ms = case.get("limitMs", problem.get("limits", {}).get("timeMs", 2000))
    elapsed_ms = 0.0
    for index, expected in enumerate(case["digests"]):
        args = batch_args(problem, batch, index)
        started = time.perf_counter()
        actual = fn(*[copy.deepcopy(args[name]) for name in order])
        elapsed_ms += (time.perf_counter() - started) * 1000.0
        if _digest(actual)[: len(expected)] != expected:
            raise AssertionError(
                "Wrong answer on random case "
                + str(index + 1)
                + " of "
                + str(len(case["digests"]))
                + ".\nInput: "
                + ", ".join(name + " = " + _short(args[name]) for name in order)
                + "\nGot: "
                + _short(actual)
            )
    if elapsed_ms > limit_ms:
        raise AssertionError(
            "Time limit exceeded: the random cases took "
            + str(int(elapsed_ms))
            + " ms, the limit is "
            + str(int(limit_ms))
            + " ms."
        )
    return elapsed_ms


def check_case(problem, case, fn):
    """Run one case. Raises AssertionError with a student-facing message on failure."""
    if "batch" in case:
        return _check_batch(problem, case, fn)
    args = {name: _materialize(value) for name, value in case["input"].items()}
    order = [p["name"] for p in problem["function"]["params"]]
    limit_ms = case.get("limitMs", problem.get("limits", {}).get("timeMs", 2000))
    show = case.get("visible", False)
    perf = case.get("perf", False)
    if perf and STATE["slow"]:
        raise AssertionError(
            "Skipped: an earlier performance test was already too slow."
        )

    reads = _Reads() if "maxReads" in case else None
    if reads:
        args = {name: _counted(value, reads) for name, value in args.items()}

    started = time.perf_counter()
    actual = fn(*[args[name] for name in order])
    elapsed_ms = (time.perf_counter() - started) * 1000.0

    if "digest" in case:
        ok = _digest(actual) == case["digest"]
        expected_text = "(large output, not shown)"
    else:
        ok = _same(
            actual,
            case["expected"],
            problem.get("compare", "exact"),
            problem.get("tolerance", 1e-9),
        )
        expected_text = _short(case["expected"])
    if not ok:
        if show:
            raise AssertionError(
                "Wrong answer.\nInput: "
                + ", ".join(name + " = " + _short(args[name]) for name in order)
                + "\nExpected: "
                + expected_text
                + "\nGot: "
                + _short(actual)
            )
        raise AssertionError("Wrong answer on a hidden test case.")
    if reads and reads.count > case["maxReads"]:
        raise AssertionError(
            "Right answer, but too many reads: your code read the list "
            + str(reads.count)
            + " times and the limit is "
            + str(case["maxReads"])
            + ". Reading every value is not allowed here: halve the search range each step (binary search)."
        )
    if elapsed_ms > limit_ms:
        if perf:
            STATE["slow"] = True
        raise AssertionError(
            "Time limit exceeded: took "
            + str(int(elapsed_ms))
            + " ms, the limit is "
            + str(int(limit_ms))
            + " ms. The answer is right but too slow: look for a faster approach."
        )
    return elapsed_ms


def load_problem(text):
    return json.loads(text)
