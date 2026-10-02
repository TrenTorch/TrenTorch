def classify_pair(a, b) -> str:
    if a is b:
        return "identical"
    if a == b:
        return "equal_not_identical"
    return "not_equal"
