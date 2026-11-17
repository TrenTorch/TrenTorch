def normalize_text(s):
    out = []
    for ch in s.lower():
        if ("a" <= ch <= "z") or ("0" <= ch <= "9"):
            out.append(ch)
        else:
            out.append(" ")
    return " ".join("".join(out).split())
