"""Contract tests for Leakage Detector."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/039-problem-39-leakage-detector').solve

def test_examples():
    assert solve(["age", "future_label", "score"]) == ["future_label"]
    assert solve(["post_clicks", "region", "TARGET_flag"]) == ["post_clicks", "TARGET_flag"]
def test_markers_are_case_insensitive():
    assert solve(["OutcomeTime", "LABEL", "safe_name"]) == ["OutcomeTime", "LABEL"]
def test_preserves_original_order():
    assert solve(["future_x", "target_y", "age"]) == ["future_x", "target_y"]
