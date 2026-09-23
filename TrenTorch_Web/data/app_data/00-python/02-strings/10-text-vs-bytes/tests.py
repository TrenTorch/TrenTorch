"""
pytest data/app_data/00-python/02-strings/10-text-vs-bytes/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
utf8_byte_length = _module.utf8_byte_length
roundtrip = _module.roundtrip
is_ascii_only = _module.is_ascii_only
first_byte_values = _module.first_byte_values


def test_byte_length_for_various_widths():
    assert utf8_byte_length("a") == 1
    assert utf8_byte_length("é") == 2
    assert utf8_byte_length("日") == 3
    assert utf8_byte_length("😀") == 4


def test_round_trip_preserves_text():
    assert roundtrip("naïve café 日本語", "utf-8") == "naïve café 日本語"


def test_lossy_encoding_does_not_raise():
    result = roundtrip("café", "ascii")
    assert "?" in result
    assert result.startswith("caf")


def test_is_ascii_only_empty_ascii_non_ascii():
    assert is_ascii_only("") is True
    assert is_ascii_only("hello") is True
    assert is_ascii_only("é") is False


def test_first_byte_values_returns_ints_and_respects_length():
    values = first_byte_values("Aé", 3)
    assert values == [65, 195, 169]
    assert all(isinstance(v, int) for v in values)
    assert first_byte_values("A", 10) == [65]
