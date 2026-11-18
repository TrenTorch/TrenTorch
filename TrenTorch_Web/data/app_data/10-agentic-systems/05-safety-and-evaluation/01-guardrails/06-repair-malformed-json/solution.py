import json
import re


def _map_outside_strings(text, fn):
    out, buf, in_str, esc = [], [], False, False
    for ch in text:
        if in_str:
            out.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            out.append(fn("".join(buf)))
            buf = []
            out.append(ch)
            in_str = True
        else:
            buf.append(ch)
    out.append(fn("".join(buf)))
    return "".join(out)


def _try(text):
    try:
        return True, json.loads(text)
    except ValueError:
        return False, None


def repair_json(text):
    ok, val = _try(text)
    if ok:
        return val
    t = text.strip()
    t = re.sub(r"^```[A-Za-z0-9_-]*\s*\n", "", t)
    t = re.sub(r"\n?```\s*$", "", t)
    ok, val = _try(t)
    if ok:
        return val
    starts = [i for i in (t.find("{"), t.find("[")) if i != -1]
    ends = [i for i in (t.rfind("}"), t.rfind("]")) if i != -1]
    if starts and ends and max(ends) > min(starts):
        t = t[min(starts):max(ends) + 1]
    ok, val = _try(t)
    if ok:
        return val
    t = _map_outside_strings(t, lambda s: re.sub(r",(\s*[}\]])", r"\1", s))
    ok, val = _try(t)
    if ok:
        return val
    t = _map_outside_strings(t, lambda s: re.sub(r"\bTrue\b", "true", re.sub(r"\bFalse\b", "false", re.sub(r"\bNone\b", "null", s))))
    ok, val = _try(t)
    if ok:
        return val
    raise ValueError("could not repair JSON")
