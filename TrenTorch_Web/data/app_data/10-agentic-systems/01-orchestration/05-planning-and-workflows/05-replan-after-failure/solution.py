def replan(plan, completed, failed_id, fallbacks):
    out = []
    for step in plan:
        if step["id"] in completed:
            continue
        new = dict(step)
        new["depends_on"] = [d for d in step["depends_on"] if d not in completed]
        if step["id"] == failed_id:
            if step["tool"] not in fallbacks:
                raise ValueError(f"no fallback for tool {step['tool']}")
            new["tool"] = fallbacks[step["tool"]]
        out.append(new)
    return out
