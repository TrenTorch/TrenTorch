def first_non_repeating_stream(s):
    out = []
    for i in range(len(s)):
        prefix = s[: i + 1]
        out.append(next((c for c in prefix if prefix.count(c) == 1), "#"))
    return "".join(out)
