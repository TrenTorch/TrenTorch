def nested_get(d: dict, path: list, default):
    """
    Follow the keys in `path` (a list of keys) one level at a
    time starting from `d`, and return the value found at the
    end. If any key along the way is missing, or an intermediate
    value is not a dictionary, return `default`. An empty `path`
    returns `d` itself. `d` must not be modified.

    Example: nested_get({"a": {"b": 1}}, ["a", "b"], 0) -> 1
             nested_get({"a": {"b": 1}}, ["a", "z"], 0) -> 0
    """
    pass


def nested_set(d: dict, path: list, value) -> None:
    """
    Store `value` at the end of the key path `path` in `d`, in
    place. Create any missing intermediate dictionaries. `path`
    has at least one key. If an intermediate value exists but is
    not a dictionary, replace it with a new dictionary. Return
    nothing.

    Example: d = {}; nested_set(d, ["a", "b"], 1)
             -> d is now {"a": {"b": 1}}
    """
    pass


def flatten_two_levels(d: dict) -> dict:
    """
    `d` maps keys to inner dictionaries (exactly two levels).
    Return a NEW single-level dictionary whose keys are
    "outer.inner" strings and whose values are the inner values,
    in traversal order.

    Example: flatten_two_levels({"a": {"x": 1, "y": 2}, "b": {"x": 3}})
             -> {"a.x": 1, "a.y": 2, "b.x": 3}
    """
    pass
