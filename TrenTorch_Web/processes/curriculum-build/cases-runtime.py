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


class TreeNode:
    """The node class used when the student's file does not define its own `TreeNode`."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def _build_tree(node_class, items):
    """A binary tree from a level-order list with None for a missing child."""
    if not items or items[0] is None:
        return None
    root = node_class(items[0])
    queue = [root]
    i = 1
    for node in queue:
        if i < len(items):
            if items[i] is not None:
                node.left = node_class(items[i])
                queue.append(node.left)
            i += 1
        if i < len(items):
            if items[i] is not None:
                node.right = node_class(items[i])
                queue.append(node.right)
            i += 1
    return root


def _tree_list(root):
    """The tree as a level-order list with None for a missing child (trailing Nones removed)."""
    out = []
    queue = [root]
    seen = set()
    for node in queue:
        if node is None:
            out.append(None)
            continue
        if id(node) in seen:
            raise AssertionError(
                "Your answer is not a tree: the same node appears twice."
            )
        seen.add(id(node))
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def _ser(vals, left, right):
    """Level-order list of the tree stored in arrays (node 0 is the root, -1 = no child)."""
    if not vals:
        return []
    out = []
    queue = [0]
    for i in queue:
        if i < 0:
            out.append(None)
            continue
        out.append(vals[i])
        queue.append(left[i])
        queue.append(right[i])
    while out and out[-1] is None:
        out.pop()
    return out


def _shape(n, rnd):
    """A random binary tree shape with n nodes: each new node takes a random free child slot."""
    left, right = [-1] * n, [-1] * n
    slots = [(0, 0), (0, 1)] if n else []
    for i in range(1, n):
        j = rnd() % len(slots)
        parent, side = slots[j]
        slots[j] = slots[-1]
        slots.pop()
        if side == 0:
            left[parent] = i
        else:
            right[parent] = i
        slots.append((i, 0))
        slots.append((i, 1))
    return left, right


def _random_bst(n, step, rnd):
    """Arrays of a random BST with the values 0, step, 2*step, ...: the root is a random value
    of the range, and each side is built the same way (the shape of inserting a random order)."""
    vals, left, right = [], [], []
    todo = [(0, n - 1, -1, 0)] if n else []
    while todo:
        lo, hi, parent, side = todo.pop()
        mid = lo + rnd() % (hi - lo + 1)
        index = len(vals)
        vals.append(mid * step)
        left.append(-1)
        right.append(-1)
        if parent >= 0:
            if side == 0:
                left[parent] = index
            else:
                right[parent] = index
        if mid + 1 <= hi:
            todo.append((mid + 1, hi, index, 1))
        if lo <= mid - 1:
            todo.append((lo, mid - 1, index, 0))
    return vals, left, right


def _preorder(vals, left, right):
    out = []
    stack = [0] if vals else []
    while stack:
        i = stack.pop()
        out.append(vals[i])
        if right[i] >= 0:
            stack.append(right[i])
        if left[i] >= 0:
            stack.append(left[i])
    return out


def _inorder(vals, left, right):
    out = []
    stack = []
    i = 0 if vals else -1
    while i >= 0 or stack:
        while i >= 0:
            stack.append(i)
            i = left[i]
        i = stack.pop()
        out.append(vals[i])
        i = right[i]
    return out


def _gen_tree(kind, spec, rnd):
    n = spec.get("n", 0)
    lo, hi = spec.get("lo", 0), spec.get("hi", 0)
    if kind == "tree_level":
        left, right = _shape(n, rnd)
        return _ser([lo + rnd() % (hi - lo + 1) for _ in range(n)], left, right)
    if kind == "tree_level_distinct":
        left, right = _shape(n, rnd)
        return _ser(_shuffle(list(range(n)), rnd), left, right)
    if kind in ("tree_preorder", "tree_inorder"):
        left, right = _shape(n, rnd)
        vals = _shuffle(list(range(n)), rnd)
        walk = _preorder if kind == "tree_preorder" else _inorder
        return walk(vals, left, right)
    if kind == "skew_tree":
        # a chain of n nodes, each the left child of the one above
        out = [rnd() % 10]
        for _ in range(n - 1):
            out.extend([rnd() % 10, None])
        return out
    if kind == "skew_bst":
        # a chain of n nodes, each the right child of the one above, values 0, step, 2*step, ...
        out = []
        for i in range(n):
            out.append(i * spec["step"])
            out.append(None)
        return out[:-1]
    if kind == "skew_preorder":
        return [i * spec["step"] for i in range(n)]
    if kind == "symmetric_tree":
        # a root whose left side is a random tree with n nodes and whose right side is its mirror;
        # sometimes one value of the mirror is changed
        left, right = _shape(n, rnd)
        small = [lo + rnd() % (hi - lo + 1) for _ in range(n)]
        vals = [lo + rnd() % (hi - lo + 1)] + small + small
        lefts, rights = [-1] * (2 * n + 1), [-1] * (2 * n + 1)
        for i in range(n):
            lefts[1 + i] = 1 + left[i] if left[i] >= 0 else -1
            rights[1 + i] = 1 + right[i] if right[i] >= 0 else -1
            lefts[1 + n + i] = 1 + n + right[i] if right[i] >= 0 else -1
            rights[1 + n + i] = 1 + n + left[i] if left[i] >= 0 else -1
        if n:
            lefts[0], rights[0] = 1, 1 + n
            if rnd() % 3 == 0:
                vals[1 + n + rnd() % n] += 1
        return _ser(vals, lefts, rights)
    vals, left, right = _random_bst(n, spec.get("step", 2), rnd)
    if kind == "bst_preorder":
        return _preorder(vals, left, right)
    if kind in ("bst_or_not", "bst_swapped") and n >= 2:
        if kind == "bst_swapped" or rnd() % 2 == 0:
            i = rnd() % n
            j = (i + 1 + rnd() % (n - 1)) % n
            vals[i], vals[j] = vals[j], vals[i]
    return _ser(vals, left, right)


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
    if kind == "cyclic_list":
        # {"values": n ints, "cycle": -1 or the position the last node points back to}
        values = [lo + rnd() % (hi - lo + 1) for _ in range(n)]
        return {"values": values, "cycle": rnd() % (n + 1) - 1}
    if kind == "joined_list":
        # {"values": n ints, "join": {...}}: the last node points at node `index` (-1 = none) of
        # the list for parameter `param`, which has `size` nodes
        values = [lo + rnd() % (hi - lo + 1) for _ in range(n)]
        index = rnd() % (spec["size"] + 1) - 1
        return {"values": values, "join": {"param": spec["param"], "index": index}}
    if kind == "repeat_but_one":
        # n + 1 different values: one appears once, the other n appear `times` times (shuffled)
        step = (hi - lo + 1) // (n + 1)
        values = [lo + i * step + rnd() % step for i in range(n + 1)]
        return _shuffle(values[:1] + values[1:] * spec["times"], rnd)
    if kind == "two_singles":
        # n + 2 different values: two appear once, the other n appear twice (shuffled)
        step = (hi - lo + 1) // (n + 2)
        values = [lo + i * step + rnd() % step for i in range(n + 2)]
        return _shuffle(values[:2] + values[2:] * 2, rnd)
    if kind == "nonzero_int_array":
        out = []
        for _ in range(n):
            v = lo + rnd() % (hi - lo + 1)
            out.append(v if v else hi)
        return out
    if kind == "choice_array":
        values = spec["values"]
        return [values[rnd() % len(values)] for _ in range(n)]
    if kind == "int_pairs_free":
        # n pairs [a, b], each of a and b in lo..hi
        pairs = []
        for _ in range(n):
            a = lo + rnd() % (hi - lo + 1)
            b = lo + rnd() % (hi - lo + 1)
            pairs.append([a, b])
        return pairs
    if kind == "int_pairs_pos":
        # n pairs [a, b] with lo <= a < b <= hi
        pairs = []
        for _ in range(n):
            a = lo + rnd() % (hi - lo)
            b = a + 1 + rnd() % (hi - a)
            pairs.append([a, b])
        return pairs
    if kind == "staircase":
        # n - 2, n - 3, ..., 1, 0, 0: every value jumps to just before the last index
        return [max(0, n - 2 - i) for i in range(n)]
    if kind == "spike_array":
        return [spec["value"] if i == spec["at"] else spec["base"] for i in range(n)]
    if kind == "jobs":
        # n jobs [deadline, profit]
        jobs = []
        for _ in range(n):
            deadline = 1 + rnd() % spec["max_deadline"]
            profit = 1 + rnd() % spec["max_profit"]
            jobs.append([deadline, profit])
        return jobs
    if kind == "k_sorted":
        # a sorted list where every value is at most k places from its sorted position
        items = sorted(lo + rnd() % (hi - lo + 1) for _ in range(n))
        size = spec["k"] + 1
        for start in range(0, n, size):
            items[start : start + size] = _shuffle(items[start : start + size], rnd)
        return items
    if kind == "stations":
        # n gas stations [position, fuel] with increasing positions below `target`
        step = max(1, spec["target"] // (n + 1))
        out = []
        for i in range(n):
            position = 1 + i * step + rnd() % step
            out.append([position, 1 + rnd() % (3 * step)])
        return out
    if kind == "straights":
        # n groups of `group` consecutive numbers, shuffled; sometimes one card is changed
        cards = []
        for _ in range(n):
            start = rnd() % 1000
            cards.extend(range(start, start + spec["group"]))
        if cards and rnd() % 3 == 0:
            cards[rnd() % len(cards)] += 1
        return _shuffle(cards, rnd)
    if kind == "duplicate_array":
        # n + 1 values from 1..n: a shuffle of 1..n plus one extra copy
        return _shuffle(list(range(1, n + 1)) + [1 + rnd() % n], rnd)
    if kind == "car_list":
        # n cars [position, speed]: different positions (multiples of `step`), speed in lo..hi
        positions = _shuffle(list(range(n)), rnd)
        return [[p * spec["step"], lo + rnd() % (hi - lo + 1)] for p in positions]
    if kind == "rpn":
        # a valid reverse Polish expression with n operands (values -9..9), never dividing by zero
        tokens, values, left = [], [], n
        while left > 0 or len(values) > 1:
            if len(values) < 2 or (left > 0 and rnd() % 2 == 0):
                v = rnd() % 19 - 9
                tokens.append(str(v))
                values.append(v)
                left -= 1
            else:
                op = "+-*/"[rnd() % 4]
                b, a = values.pop(), values.pop()
                if op == "/" and b == 0:
                    op = "+"
                if op == "*" and abs(a * b) > 10**9:
                    op = "+"
                if op == "+":
                    r = a + b
                elif op == "-":
                    r = a - b
                elif op == "*":
                    r = a * b
                else:
                    q = abs(a) // abs(b)
                    r = q if (a < 0) == (b < 0) else -q
                tokens.append(op)
                values.append(r)
        return tokens
    if kind == "path_string":
        # an absolute Unix path with n names, some of them . or .., maybe a trailing slash
        names = ["a", "b", "c", "d", ".", "..", ".", "..", "..."]
        path = ""
        for _ in range(n):
            path += "/" * (1 + rnd() % 2) + names[rnd() % len(names)]
        if not path:
            path = "/"
        if rnd() % 4 == 0:
            path += "/"
        return path
    if kind == "nested_encoding":
        # a valid k[text] string with n top-level items, nested up to 4 levels, counts 1..3

        def seq(items, depth):
            out = []
            for _ in range(items):
                if depth < 4 and rnd() % 3 == 0:
                    count = 1 + rnd() % 3
                    out.append(str(count) + "[" + seq(1 + rnd() % 3, depth + 1) + "]")
                else:
                    out.append("".join("abc"[rnd() % 3] for _ in range(1 + rnd() % 2)))
            return "".join(out)

        return seq(n, 0)
    if kind == "stack_ops":
        # a valid list of operations for a stack with minimum ("min_stack") or a queue ("queue")
        ops, size = [], 0
        for _ in range(n):
            if spec["kind"] == "min_stack":
                if size == 0 or rnd() % 5 < 2:
                    ops.append("push " + str(rnd() % 21 - 10))
                    size += 1
                else:
                    r = rnd() % 3
                    if r == 0:
                        ops.append("pop")
                        size -= 1
                    else:
                        ops.append("top" if r == 1 else "get_min")
            else:
                if size == 0:
                    if rnd() % 2 == 0:
                        ops.append("push " + str(rnd() % 21 - 10))
                        size += 1
                    else:
                        ops.append("empty")
                else:
                    r = rnd() % 5
                    if r < 2:
                        ops.append("push " + str(rnd() % 21 - 10))
                        size += 1
                    elif r == 2:
                        ops.append("pop")
                        size -= 1
                    else:
                        ops.append("peek" if r == 3 else "empty")
        return ops
    if kind == "arith_expr":
        # n operands 1..hi joined by random operators from `ops`, no spaces
        parts = [str(1 + rnd() % hi)]
        for _ in range(n - 1):
            parts.append(spec["ops"][rnd() % len(spec["ops"])])
            parts.append(str(1 + rnd() % hi))
        return "".join(parts)
    if kind == "calc_expr":
        # n operands 1..hi with + and -, brackets, and minus signs after "(" or at the start

        def build(k):
            if k == 1:
                return str(1 + rnd() % hi)
            a = 1 + rnd() % (k - 1)
            left, right = build(a), build(k - a)
            op = "+" if rnd() % 2 == 0 else "-"
            if a > 1 and rnd() % 2 == 0:
                left = "(" + ("-" if rnd() % 6 == 0 else "") + left + ")"
            if k - a > 1 and (op == "-" or rnd() % 2 == 0):
                right = "(" + ("-" if rnd() % 6 == 0 else "") + right + ")"
            return left + op + right

        text = build(n)
        return "-" + text if rnd() % 8 == 0 else text
    if kind in (
        "tree_level",
        "tree_level_distinct",
        "symmetric_tree",
        "skew_tree",
        "tree_preorder",
        "tree_inorder",
        "bst_level",
        "bst_or_not",
        "bst_swapped",
        "bst_preorder",
        "skew_bst",
        "skew_preorder",
    ):
        return _gen_tree(kind, spec, rnd)
    if kind == "word_list":
        alphabet = spec["alphabet"]
        words = [
            "".join(alphabet[rnd() % len(alphabet)] for _ in range(spec["length"]))
            for _ in range(n)
        ]
        return words + spec.get("extra", [])
    if kind == "sparse_blocks":
        # rows x cols grid of 0 and 1 where `percent` percent of the cells are 1
        return [
            [1 if rnd() % 100 < spec["percent"] else 0 for _ in range(spec["cols"])]
            for _ in range(spec["rows"])
        ]
    if kind == "one_zero_matrix":
        # rows x cols grid of 0 and 1 where `percent` percent are 0 and at least one cell is 0
        rows, cols = spec["rows"], spec["cols"]
        grid = [
            [0 if rnd() % 100 < spec["percent"] else 1 for _ in range(cols)]
            for _ in range(rows)
        ]
        if rows and cols:
            grid[rnd() % rows][rnd() % cols] = 0
        return grid
    if kind == "permutation_grid":
        rows, cols = spec["rows"], spec["cols"]
        flat = _shuffle(list(range(rows * cols)), rnd)
        return [flat[r * cols : (r + 1) * cols] for r in range(rows)]
    if kind in ("weighted_edges", "positive_edges", "signed_edges"):
        # n edges [a, b, w] between different nodes of 0..nodes-1: w in 0..max_w, 1..max_w or
        # -max_w..max_w
        nodes, max_w = spec["nodes"], spec["max_w"]
        edges = []
        for _ in range(n):
            a = rnd() % nodes
            b = rnd() % (nodes - 1)
            if b >= a:
                b += 1
            if kind == "weighted_edges":
                w = rnd() % (max_w + 1)
            elif kind == "positive_edges":
                w = 1 + rnd() % max_w
            else:
                w = rnd() % (2 * max_w + 1) - max_w
            edges.append([a, b, w])
        return edges
    if kind == "forest_edges":
        # n edges forming a tree on the nodes 0..n
        return [[i, rnd() % i] for i in range(1, n + 1)]
    if kind == "dag_edges":
        # n directed edges between different nodes that all follow one hidden order, plus (with
        # probability cycle_chance percent) one reversed copy of a random edge, which makes a cycle
        nodes = spec["nodes"]
        rank = _shuffle(list(range(nodes)), rnd)
        edges = []
        for _ in range(n):
            a = rnd() % nodes
            b = rnd() % (nodes - 1)
            if b >= a:
                b += 1
            edges.append([a, b] if rank[a] < rank[b] else [b, a])
        if edges and rnd() % 100 < spec["cycle_chance"]:
            a, b = edges[rnd() % len(edges)]
            edges.append([b, a])
        return edges
    if kind == "bipartite_edges":
        # n edges between the even nodes and the odd nodes of 0..nodes-1
        half = spec["nodes"] // 2
        return [[2 * (rnd() % half), 2 * (rnd() % half) + 1] for _ in range(n)]
    if kind == "alien_words":
        # n words sorted by a hidden random alphabet order (sometimes shuffled instead)
        alphabet = spec["alphabet"]
        order = _shuffle(list(alphabet), rnd)
        rank = {ch: i for i, ch in enumerate(order)}
        words = [
            "".join(
                alphabet[rnd() % len(alphabet)]
                for _ in range(1 + rnd() % spec["max_len"])
            )
            for _ in range(n)
        ]
        words.sort(key=lambda w: [rank[ch] for ch in w])
        if rnd() % 4 == 0:
            _shuffle(words, rnd)
        return words
    if kind == "tree_plus_edge":
        # a tree on the nodes 1..n plus one more edge, in shuffled order
        edges = [[1 + rnd() % (i - 1), i] for i in range(2, n + 1)]
        a = 1 + rnd() % n
        b = 1 + rnd() % (n - 1)
        if b >= a:
            b += 1
        edges.append([a, b])
        return _shuffle(edges, rnd)
    if kind == "distinct_cells":
        # n different cells [x, y] with 0 <= x, y <= limit
        seen, cells = set(), []
        while len(cells) < n:
            cell = (rnd() % (spec["limit"] + 1), rnd() % (spec["limit"] + 1))
            if cell not in seen:
                seen.add(cell)
                cells.append([cell[0], cell[1]])
        return cells
    if kind == "equation_list":
        # n equations such as "a==b" or "c!=d" over the letters of `alphabet`
        alphabet = spec["alphabet"]
        out = []
        for _ in range(n):
            a = alphabet[rnd() % len(alphabet)]
            op = "==" if rnd() % 2 == 0 else "!="
            b = alphabet[rnd() % len(alphabet)]
            out.append(a + op + b)
        return out
    if kind == "connected_edges":
        # a connected weighted graph on 0..nodes-1 (node 0 reaches every node): a random tree with arrows
        # away from node 0, plus extra edges, up to n edges
        nodes, max_w = spec["nodes"], spec["max_w"]
        edges = [[rnd() % i, i, 1 + rnd() % max_w] for i in range(1, nodes)]
        while len(edges) < n:
            a = rnd() % nodes
            b = rnd() % (nodes - 1)
            if b >= a:
                b += 1
            edges.append([a, b, 1 + rnd() % max_w])
        return _shuffle(edges, rnd)
    if kind == "connected_simple_edges":
        # a random tree on n nodes plus `extra` more different edges (no repeats), shuffled
        edges = [[rnd() % i, i] for i in range(1, n)]
        have = {(a, b) for a, b in edges}
        for _ in range(spec["extra"]):
            for _ in range(20):
                a = rnd() % n
                b = rnd() % (n - 1)
                if b >= a:
                    b += 1
                low, high = min(a, b), max(a, b)
                if (low, high) not in have:
                    have.add((low, high))
                    edges.append([low, high])
                    break
        return _shuffle(edges, rnd)
    if kind == "path_edges":
        return [[i, i + 1] for i in range(n - 1)]
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


class ListNode:
    """The node class used when the student's file does not define its own `ListNode`."""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def _build_list(node_class, spec, built):
    """A linked list from JSON: a list of values, or {"values": [...], "cycle": k} (the tail
    points back at node k) or {"values": [...], "join": {"param": "a", "index": k}} (the tail
    points at node k of the list already built for parameter "a"; with no values of its own, the
    head is that node). Returns (head, nodes it made)."""
    values = _materialize(spec["values"] if isinstance(spec, dict) else spec)
    nodes = [node_class(value) for value in values]
    for left, right in zip(nodes, nodes[1:]):
        left.next = right
    tail = None
    if isinstance(spec, dict):
        if nodes and spec.get("cycle", -1) >= 0:
            nodes[-1].next = nodes[spec["cycle"]]
        join = spec.get("join")
        if join and join["index"] >= 0:
            tail = built[join["param"]][join["index"]]
            if nodes:
                nodes[-1].next = tail
    return (nodes[0] if nodes else tail), nodes


def _prepare(problem, fn, raw):
    """The arguments to call fn with. Parameters of type ListNode or TreeNode become linked lists
    and trees made from the student's own ListNode or TreeNode class (or the ones above).
    Returns (arguments, nodes), where nodes maps each ListNode parameter to its list of nodes."""
    params = problem["function"]["params"]
    kinds = ("ListNode", "list[ListNode]", "TreeNode")
    if not any(p["type"] in kinds for p in params):
        return raw, None
    scope = getattr(fn, "__globals__", {})
    args, built = dict(raw), {}
    for p in params:
        if p["type"] == "ListNode":
            args[p["name"]], built[p["name"]] = _build_list(
                scope.get("ListNode", ListNode), raw[p["name"]], built
            )
        elif p["type"] == "list[ListNode]":
            node_class = scope.get("ListNode", ListNode)
            lists = [_build_list(node_class, spec, built) for spec in raw[p["name"]]]
            args[p["name"]] = [head for head, _ in lists]
        elif p["type"] == "TreeNode":
            args[p["name"]] = _build_tree(
                scope.get("TreeNode", TreeNode), raw[p["name"]]
            )
    return args, built


def _list_values(head):
    values, seen = [], set()
    while head is not None:
        if id(head) in seen:
            raise AssertionError(
                "Your answer is a list that loops back on itself. Check the last next pointer."
            )
        seen.add(id(head))
        values.append(head.val)
        head = head.next
    return values


def _finish(problem, actual, built):
    """The answer as plain JSON: a returned ListNode becomes its list of values, and a returned
    ListNodeRef becomes its position in the first list parameter (-1 for None)."""
    kind = problem["function"]["returns"]
    if kind == "TreeNode":
        return _tree_list(actual)
    if kind == "TreeNodeVal":
        return None if actual is None else actual.val
    if kind == "ListNode":
        return _list_values(actual)
    if kind == "ListNodeRef":
        if actual is None:
            return -1
        first = next(iter(built.values()))
        for index, node in enumerate(first):
            if node is actual:
                return index
        raise AssertionError(
            "The node you returned is not a node of the list you were given."
        )
    return actual


def call_fn(problem, fn, raw):
    """Run fn on JSON inputs and return the answer as JSON (used by the authoring tools)."""
    args, built = _prepare(problem, fn, raw)
    order = [p["name"] for p in problem["function"]["params"]]
    return _finish(problem, fn(*[args[name] for name in order]), built)


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
        call_args, built = _prepare(problem, fn, copy.deepcopy(args))
        started = time.perf_counter()
        actual = fn(*[call_args[name] for name in order])
        elapsed_ms += (time.perf_counter() - started) * 1000.0
        actual = _finish(problem, actual, built)
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

    call_args, built = _prepare(problem, fn, args)
    started = time.perf_counter()
    actual = fn(*[call_args[name] for name in order])
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    actual = _finish(problem, actual, built)

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
