"""Contract tests for Group Aggregation."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
solve = load_solution('17-data-statistics-for-data-science/01-data-statistics/040-problem-40-group-aggregation').solve

def test_examples():
    assert solve(["a","a","b"], [1.,2.,4.]) == {"a":1.5,"b":4.}
    assert solve(["north","south","north"], [10,6,14]) == {"north":12.,"south":6.}
def test_single_value_groups():
    assert solve(["x","y"], [3.,8.]) == {"x":3.,"y":8.}
def test_negative_and_repeated_values():
    assert solve([1,1,1], [-2.,0.,2.]) == {1:0.}
