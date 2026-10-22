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


def _gen(spec):
    rnd = _mulberry32(spec.get("seed", 1))
    kind = spec["type"]
    n = spec.get("n", 0)
    lo, hi = spec.get("lo", 0), spec.get("hi", 0)
    if kind == "int_array":
        return [lo + rnd() % (hi - lo + 1) for _ in range(n)]
    if kind == "sorted_int_array":
        return sorted(lo + rnd() % (hi - lo + 1) for _ in range(n))
    if kind == "string":
        alphabet = spec["alphabet"]
        return "".join(alphabet[rnd() % len(alphabet)] for _ in range(n))
    if kind == "permutation":
        # a shuffle of 0..n-1 (Fisher-Yates driven by the portable PRNG)
        items = list(range(n))
        for i in range(n - 1, 0, -1):
            j = rnd() % (i + 1)
            items[i], items[j] = items[j], items[i]
        return items
    if kind == "int_matrix":
        return [
            [lo + rnd() % (hi - lo + 1) for _ in range(spec["cols"])]
            for _ in range(spec["rows"])
        ]
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
