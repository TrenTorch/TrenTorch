"""
pytest tests.py
"""

import pytest

from _load import load_solution

_module = load_solution(__file__)
Recorder = _module.Recorder
SuppressAndRecord = _module.SuppressAndRecord
temporary_value = _module.temporary_value
write_lines = _module.write_lines
read_lines = _module.read_lines


def test_recorder_normal_path():
    log = []
    with Recorder(log) as r:
        assert isinstance(r, Recorder)
    assert log == ["enter", "exit"]


def test_recorder_on_exception():
    log = []
    with pytest.raises(ValueError):
        with Recorder(log):
            raise ValueError("boom")
    assert log == ["enter", "exit", "error:ValueError"]


def test_suppress_and_record_selectivity():
    ctx = SuppressAndRecord(ValueError)
    with ctx:
        raise ValueError("boom")
    assert isinstance(ctx.caught, ValueError)

    ctx2 = SuppressAndRecord(ValueError)
    with pytest.raises(TypeError):
        with ctx2:
            raise TypeError("nope")
    assert ctx2.caught is None


def test_temporary_value_restores_after_success_and_failure():
    settings = {"mode": "a"}
    with temporary_value(settings, "mode", "b"):
        assert settings["mode"] == "b"
    assert settings["mode"] == "a"

    with pytest.raises(ValueError):
        with temporary_value(settings, "mode", "c"):
            assert settings["mode"] == "c"
            raise ValueError("boom")
    assert settings["mode"] == "a"


def test_file_round_trip(tmp_path):
    path = str(tmp_path / "out.txt")
    lines = ["hello", "", "café"]
    write_lines(path, lines)
    assert read_lines(path) == lines

    empty_path = str(tmp_path / "empty.txt")
    write_lines(empty_path, [])
    assert read_lines(empty_path) == []


def test_cleanup_is_guaranteed_with_return():
    log = []

    def run():
        with Recorder(log):
            return "done"

    assert run() == "done"
    assert log == ["enter", "exit"]
