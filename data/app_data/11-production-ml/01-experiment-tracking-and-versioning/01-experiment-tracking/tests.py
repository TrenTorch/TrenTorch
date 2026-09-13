"""
pytest data/app_data/11-production-ml/01-experiment-tracking-and-versioning/01-experiment-tracking/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/01-experiment-tracking-and-versioning/{Path(__file__).resolve().parent.name}")
create_run = _module.create_run
log_metric = _module.log_metric
log_artifact = _module.log_artifact
get_metric_history = _module.get_metric_history
get_latest_metric = _module.get_latest_metric


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_create_run_stores_hyperparameters():
    run = create_run("run-1", {"lr": 0.01, "batch_size": 32})
    assert run["run_id"] == "run-1"
    assert run["hyperparameters"] == {"lr": 0.01, "batch_size": 32}


def test_02_log_metric_builds_a_history():
    run = create_run("run-2", {})
    log_metric(run, "loss", 1.0, step=0)
    log_metric(run, "loss", 0.5, step=1)
    assert get_metric_history(run, "loss") == [(0, 1.0), (1, 0.5)]


# --- General-case coverage --------------------------------------------


def test_03_log_artifact_overwrites_same_name():
    run = create_run("run-3", {})
    log_artifact(run, "checkpoint", "/tmp/ckpt_v1.pt")
    log_artifact(run, "checkpoint", "/tmp/ckpt_v2.pt")
    assert run["artifacts"]["checkpoint"] == "/tmp/ckpt_v2.pt"


def test_04_get_latest_metric_uses_highest_step_not_last_appended():
    run = create_run("run-4", {})
    log_metric(run, "acc", 0.9, step=5)
    log_metric(run, "acc", 0.8, step=2)  # appended out of order
    assert get_latest_metric(run, "acc") == 0.9


def test_05_different_metrics_have_independent_histories():
    run = create_run("run-5", {})
    log_metric(run, "loss", 1.0, step=0)
    log_metric(run, "accuracy", 0.5, step=0)
    assert get_metric_history(run, "loss") == [(0, 1.0)]
    assert get_metric_history(run, "accuracy") == [(0, 0.5)]


# --- Parameter handling -------------------------------------------------


def test_06_hyperparameters_are_copied_not_aliased():
    original = {"lr": 0.01}
    run = create_run("run-6", original)
    original["lr"] = 999.0
    assert run["hyperparameters"]["lr"] == 0.01


def test_07_multiple_artifacts_coexist_by_name():
    run = create_run("run-7", {})
    log_artifact(run, "model", "/tmp/model.pt")
    log_artifact(run, "plot", "/tmp/plot.png")
    assert run["artifacts"] == {"model": "/tmp/model.pt", "plot": "/tmp/plot.png"}


# --- Edge cases ---------------------------------------------------------


def test_08_get_metric_history_for_unlogged_metric_is_empty():
    run = create_run("run-8", {})
    assert get_metric_history(run, "never_logged") == []


def test_09_get_latest_metric_raises_for_unlogged_metric():
    run = create_run("run-9", {})
    with pytest.raises(KeyError):
        get_latest_metric(run, "never_logged")


# --- Independent correctness oracle -----------------------------------


def test_10_metric_history_accumulates_rather_than_overwrites():
    # Directly targets a mutant that treats log_metric like
    # log_artifact (overwriting instead of appending) -- a metric
    # logged at many different steps must retain EVERY measurement.
    run = create_run("run-10", {})
    for step in range(10):
        log_metric(run, "loss", 1.0 / (step + 1), step=step)
    history = get_metric_history(run, "loss")
    assert len(history) == 10
    assert history[0] == (0, 1.0)
    assert history[-1] == (9, 0.1)
