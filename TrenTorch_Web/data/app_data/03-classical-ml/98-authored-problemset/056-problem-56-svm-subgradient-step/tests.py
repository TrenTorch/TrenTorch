"""Oracle cases captured by executing the supplied reference implementation."""
import sys
from pathlib import Path
import numpy as np, pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from _load import load_solution
class Param:
 def __init__(self,requires_grad):self.requires_grad=requires_grad
def variant(v,mode):
 if isinstance(v,np.ndarray):return v[::-1].copy() if mode==1 and v.ndim else (np.zeros_like(v) if mode==2 and v.dtype.kind in "iufcb" else v.copy())
 if isinstance(v,list):return list(reversed(v)) if mode==1 else ([0 for _ in v] if all(isinstance(x,(int,float,np.number,bool)) for x in v) else [variant(x,mode) for x in v])
 if isinstance(v,tuple):return tuple(variant(x,mode) for x in v)
 if isinstance(v,float):return v*.75 if mode==1 else v
 return v
def same(a,e):
 if isinstance(e,dict) and "param" in e:assert a.requires_grad is e["param"];return
 if isinstance(e,dict) and "tuple" in e:
  assert isinstance(a,tuple) and len(a)==len(e["tuple"])
  for x,y in zip(a,e["tuple"]):same(x,y)
  return
 if isinstance(e,dict) and "nan" in e:assert np.isnan(a);return
 if isinstance(e,list):
  assert len(a)==len(e)
  for x,y in zip(a,e):same(x,y)
  return
 if isinstance(e,(int,float,np.number)) and not isinstance(e,bool):np.testing.assert_allclose(a,e,rtol=1e-7,atol=1e-8,equal_nan=True);return
 assert a==e
solve=load_solution("03-classical-ml/98-authored-problemset/056-problem-56-svm-subgradient-step").solve

def test_01_visible_case():
 args=([[1,0],[0,1]],[1,-1],[0,0],.1,.01)
 same(solve(*args),[0.001, -0.001])

def test_02_visible_case():
 args=tuple(variant(v,1) for v in eval('([[1,0],[0,1]],[1,-1],[0,0],.1,.01)',globals()))
 same(solve(*args),[0.0005625000000000001, -0.0005625000000000001])

def test_03_hidden_case():
 args=tuple(variant(v,2) for v in eval('([[1,0],[0,1]],[1,-1],[0,0],.1,.01)',globals()))
 same(solve(*args),[0.0, 0.0])
