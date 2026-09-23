"""
pytest data/app_data/99-potd/01-daily/27-run-logger-json/tests.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
build_run_record = _module.build_run_record


def test_example_matches_the_specs_worked_record():
    record = build_run_record("run_0042", [("lr", "0.001"), ("batch_size", "64")], [("val_loss", "0.231")])
    assert record == {
        "run_id": "run_0042",
        "hyperparameters": {"batch_size": "64", "lr": "0.001"},
        "metrics": {"val_loss": "0.231"},
    }
    # must also be JSON-serializable and structurally equal after a round trip
    assert json.loads(json.dumps(record)) == record


def test_empty_hyperparameters_and_metrics_give_empty_objects():
    record = build_run_record("run_0001", [], [])
    assert record == {"run_id": "run_0001", "hyperparameters": {}, "metrics": {}}
    assert "hyperparameters" in record
    assert "metrics" in record


def test_duplicate_keys_keep_the_last_value():
    record = build_run_record("run_dup", [("lr", "0.1"), ("lr", "0.01")], [])
    assert record["hyperparameters"] == {"lr": "0.01"}


def test_output_keys_are_sorted_even_when_insertion_order_differs():
    record = build_run_record(
        "run_sort",
        [("zeta", "1"), ("alpha", "2"), ("mid", "3")],
        [("z_metric", "9"), ("a_metric", "1")],
    )
    assert list(record["hyperparameters"].keys()) == ["alpha", "mid", "zeta"]
    assert list(record["metrics"].keys()) == ["a_metric", "z_metric"]


def test_only_hyperparameters_empty():
    record = build_run_record("run_x", [], [("acc", "0.9")])
    assert record["hyperparameters"] == {}
    assert record["metrics"] == {"acc": "0.9"}
