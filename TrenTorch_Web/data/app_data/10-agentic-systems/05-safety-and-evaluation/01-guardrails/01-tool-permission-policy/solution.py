from fnmatch import fnmatchcase


def check_permission(call, policy):
    for decision in ("deny", "ask", "allow"):
        if any(fnmatchcase(call, p) for p in policy.get(decision, [])):
            return decision
    return "deny"
