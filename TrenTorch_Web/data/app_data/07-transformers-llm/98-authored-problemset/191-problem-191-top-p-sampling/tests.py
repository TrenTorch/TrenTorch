"""Question-specific tests with fixed expected values."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution
_module = load_solution('07-transformers-llm/98-authored-problemset/191-problem-191-top-p-sampling')
solve = _module.solve
CASES = [
    ("example_1", [[0.0, 1.0, 2.0], 0.7, {'$rng': 3}], 1),
    ("example_2", [[0.0, 5.0, -2.0], 0.2, {'$rng': 0}], 1),
]
def _build(x):
    if isinstance(x,dict) and set(x)=={"$rng"}: return np.random.default_rng(x["$rng"])
    if isinstance(x,dict) and set(x)=={"$quadratic"}: return lambda v: float(np.sum(np.asarray(v,dtype=float)**2))
    if isinstance(x,list): return [_build(v) for v in x]
    if isinstance(x,dict): return {k:_build(v) for k,v in x.items()}
    return x
def _assert_value(actual,expected):
    if isinstance(actual,tuple):
        assert isinstance(expected,list) and len(actual)==len(expected)
        for a,e in zip(actual,expected): _assert_value(a,e)
    elif isinstance(actual,dict): assert actual==expected
    elif isinstance(expected,list): np.testing.assert_allclose(np.asarray(actual),np.asarray(expected),rtol=1e-7,atol=1e-9)
    elif isinstance(expected,float): assert actual==pytest.approx(expected,rel=1e-7,abs=1e-9)
    else: assert actual==expected
@pytest.mark.parametrize("case,args,expected",CASES,ids=[x[0] for x in CASES])
def test_contract(case,args,expected): _assert_value(solve(*_build(args)),expected)
