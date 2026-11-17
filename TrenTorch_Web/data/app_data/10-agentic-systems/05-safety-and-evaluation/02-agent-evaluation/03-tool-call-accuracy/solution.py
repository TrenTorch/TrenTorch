import json
from collections import Counter


def _prf(pred, exp):
    matches = sum((Counter(pred) & Counter(exp)).values())
    p = matches / len(pred) if pred else 0.0
    r = matches / len(exp) if exp else 0.0
    f = 0.0 if p + r == 0 else 2 * p * r / (p + r)
    return p, r, f


def tool_call_metrics(predicted, expected):
    if not predicted and not expected:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0, "name_f1": 1.0}
    key = lambda call: (call[0], json.dumps(call[1], sort_keys=True))
    p, r, f = _prf([key(c) for c in predicted], [key(c) for c in expected])
    _, _, nf = _prf([c[0] for c in predicted], [c[0] for c in expected])
    return {"precision": p, "recall": r, "f1": f, "name_f1": nf}
