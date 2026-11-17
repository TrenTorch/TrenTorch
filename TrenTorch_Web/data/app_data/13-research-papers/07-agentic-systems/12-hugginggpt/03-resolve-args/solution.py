def resolve_args(args, results):
    out = args
    for tid, value in results.items():
        out = out.replace(f"<{tid}>", str(value))
    return out
