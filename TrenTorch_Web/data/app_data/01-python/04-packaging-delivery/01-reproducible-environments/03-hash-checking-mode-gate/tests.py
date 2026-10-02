"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
check_hash_mode = _module.check_hash_mode


def req(name, spec="", hashes=()):
    return {"name": name, "spec": spec, "hashes": list(hashes)}


def test_inactive_when_no_hashes_anywhere():
    assert check_hash_mode([req("numpy", ">=1.0"), req("pandas")]) == []


def test_empty_list_is_fine():
    assert check_hash_mode([]) == []


def test_fully_pinned_and_hashed_passes():
    reqs = [req("numpy", "==1.26.4", ["sha256:aa"]), req("pandas", "==2.2.0", ["sha256:bb"])]
    assert check_hash_mode(reqs) == []


def test_one_hash_activates_the_mode_for_everyone():
    reqs = [req("numpy", "==1.26.4", ["sha256:aa"]), req("pandas", "==2.2.0")]
    assert check_hash_mode(reqs) == ["pandas: missing hash"]


def test_unpinned_requirement_is_reported():
    reqs = [req("numpy", "==1.26.4", ["sha256:aa"]), req("pandas", ">=2.0", ["sha256:bb"])]
    assert check_hash_mode(reqs) == ["pandas: not pinned"]


def test_both_errors_for_one_requirement_in_order():
    reqs = [req("zlib-thing"), req("numpy", "==1.0", ["sha256:aa"])]
    assert check_hash_mode(reqs) == ["zlib-thing: not pinned", "zlib-thing: missing hash"]


def test_errors_sorted_by_name_and_wildcard_not_pinned():
    reqs = [req("b", "==1.*", ["sha256:aa"]), req("a", "==1.0")]
    assert check_hash_mode(reqs) == ["a: missing hash", "b: not pinned"]
