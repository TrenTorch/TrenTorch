def _type_ok(value, t):
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, {"string": str, "boolean": bool, "array": list}.get(t, object))


def validate_arguments(args, schema):
    props = schema.get("properties", {})
    errors = [f"missing: {n}" for n in schema.get("required", []) if n not in args]
    for name, value in args.items():
        if name not in props:
            errors.append(f"unexpected: {name}")
            continue
        spec = props[name]
        if not _type_ok(value, spec.get("type")):
            errors.append(f"type: {name}")
        elif "enum" in spec and value not in spec["enum"]:
            errors.append(f"enum: {name}")
        elif spec.get("type") in ("integer", "number") and (
            ("minimum" in spec and value < spec["minimum"]) or ("maximum" in spec and value > spec["maximum"])
        ):
            errors.append(f"range: {name}")
    return sorted(errors)
