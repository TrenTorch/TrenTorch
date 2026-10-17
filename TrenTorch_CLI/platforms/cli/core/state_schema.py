"""Shape validators for the CLI's own state files.

read_json_or_warn() already warns and falls back when a state file
fails to parse. These validators close the other half of that gap:
a file that parses but has the wrong *shape* (a list at the root, a
null where a list belongs, a string where a list belongs) used to
reach callers that assume a dict with list/dict fields, crashing
with AttributeError/TypeError -- or, for string values, silently
doing substring membership instead of list membership.

Each validator returns the (possibly repaired) dict, or None if the
root isn't an object at all. read_json_or_warn treats None the same
as a parse failure: warn, fall back to the caller's default.
"""

_PROGRESS_LIST_FIELDS = ("started_modules", "completed_modules", "completion_dates")

_MILESTONE_LIST_FIELDS = ("completed_milestones", "unlocked_milestones", "achievements")
_MILESTONE_DICT_FIELDS = ("completion_dates", "unlock_dates")


def validate_progress(data):
    """Ensure progress.json has the shape the CLI assumes.

    Returns (data, repaired_keys), where repaired_keys lists the fields
    that were reset. Returns None if the root isn't an object at all
    (the caller then falls back to its own default).
    """
    if not isinstance(data, dict):
        return None
    repaired = []
    for key in _PROGRESS_LIST_FIELDS:
        if not isinstance(data.get(key), list):
            data[key] = []
            repaired.append(key)
    return data, repaired


def validate_milestones(data):
    """Ensure milestones.json has the shape the CLI assumes.

    Returns (data, repaired_keys), or None if the root isn't an object.
    """
    if not isinstance(data, dict):
        return None
    repaired = []
    for key in _MILESTONE_LIST_FIELDS:
        if not isinstance(data.get(key), list):
            data[key] = []
            repaired.append(key)
    for key in _MILESTONE_DICT_FIELDS:
        if not isinstance(data.get(key), dict):
            data[key] = {}
            repaired.append(key)
    if not isinstance(data.get("total_unlocked"), int):
        data["total_unlocked"] = 0
        repaired.append("total_unlocked")
    return data, repaired