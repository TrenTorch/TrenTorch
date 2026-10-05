def _coerce(value, t):
    if t == "integer":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return value
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
    if t == "number":
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return value
        return value
    if t == "boolean":
        if isinstance(value, str):
            low = value.lower()
            if low in ("true", "yes", "1"):
                return True
            if low in ("false", "no", "0"):
                return False
        return value
    return value


def coerce_arguments(args, schema):
    out = {k: (_coerce(v, schema[k]["type"]) if k in schema else v) for k, v in args.items()}
    for name, spec in schema.items():
        if name not in out and "default" in spec:
            out[name] = spec["default"]
    return out
