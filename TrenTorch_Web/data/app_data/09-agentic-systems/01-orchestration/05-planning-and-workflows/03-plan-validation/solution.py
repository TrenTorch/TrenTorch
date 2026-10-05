def validate_plan(plan, tools):
    errors, seen = [], set()
    for step in plan:
        sid, tool = step["id"], step["tool"]
        if tool not in tools:
            errors.append(f"step {sid}: unknown tool '{tool}'")
        else:
            spec = tools[tool]
            required, optional = set(spec.get("required", [])), set(spec.get("optional", []))
            args = set(step.get("args", {}))
            for a in sorted(required - args):
                errors.append(f"step {sid}: missing argument '{a}'")
            for a in sorted(args - required - optional):
                errors.append(f"step {sid}: unexpected argument '{a}'")
        for d in step.get("depends_on", []):
            if d not in seen:
                errors.append(f"step {sid}: invalid dependency '{d}'")
        seen.add(sid)
    return errors
