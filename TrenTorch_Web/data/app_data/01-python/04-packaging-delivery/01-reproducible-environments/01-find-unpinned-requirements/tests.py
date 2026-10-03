"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
find_unpinned = _module.find_unpinned


def test_exact_pins_are_fine():
    assert find_unpinned(["numpy==1.26.4", "torch == 2.3.0"]) == []


def test_ranges_and_bare_names_are_unpinned_in_order():
    reqs = ["numpy==1.26.4", "pandas>=2.0", "requests", "scipy~=1.11"]
    assert find_unpinned(reqs) == ["pandas>=2.0", "requests", "scipy~=1.11"]


def test_wildcard_and_compound_specs_are_not_exact():
    assert find_unpinned(["scipy==1.*", "foo==1.0,<2"]) == ["scipy==1.*", "foo==1.0,<2"]


def test_blank_comment_and_option_lines_ignored():
    reqs = ["", "   ", "# a comment", "--require-hashes", "-r other.txt", "numpy==1.0"]
    assert find_unpinned(reqs) == []


def test_inline_comment_hash_option_and_backslash_are_stripped():
    reqs = [
        "torch==2.3.0 --hash=sha256:abc123 \\",
        "pandas>=2.0  # needs a pin",
    ]
    assert find_unpinned(reqs) == ["pandas>=2.0"]


def test_direct_reference_counts_as_pinned():
    assert find_unpinned(["mypkg @ https://example.com/mypkg-1.0-py3-none-any.whl"]) == []


def test_extras_and_markers():
    reqs = [
        "uvicorn[standard]==0.30.1",
        "bar==1.0 ; python_version < '3.9'",
        "baz[extra]>=1 ; sys_platform == 'win32'",
    ]
    assert find_unpinned(reqs) == ["baz[extra]>=1"]
