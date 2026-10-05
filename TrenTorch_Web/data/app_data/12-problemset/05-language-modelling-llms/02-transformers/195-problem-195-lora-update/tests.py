"""Question-specific tests with fixed expected values."""
import numpy as np
import pytest
from _load import load_solution
_module=load_solution(__file__)
solve=_module.solve
CASES=[
    ("example_1", [[1.0, 2.0], [[1.0, 0.0], [0.0, 1.0]], [[2.0, 1.0], [0.0, 3.0]]], [4.0, 6.0]),
    ("example_2", [[0.0, 0.0], [[1.0, 1.0]], [[2.0], [3.0]]], [0.0, 0.0]),
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
def test_contract(case,args,expected):
    if 195 in (194,195,230,250):
        if 195==194: args=[np.asarray(args[0]),np.asarray(args[1])]
        elif 195==195: args=[np.asarray(x) for x in args]
        elif 195==230: args=[np.asarray(args[0]),np.asarray(args[1]),args[2]]
        else: args=[_build(args[0]),np.asarray(args[1]),np.asarray(args[2]),args[3]]
    _assert_value(solve(*_build(args)),expected)
