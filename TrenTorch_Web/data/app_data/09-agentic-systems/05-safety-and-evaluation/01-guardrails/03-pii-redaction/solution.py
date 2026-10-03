import re


def luhn_valid(digits):
    if not digits.isdigit() or not 13 <= len(digits) <= 19:
        return False
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def redact_pii(text):
    counts = {}

    def sub(pattern, label, check=None):
        nonlocal text

        def repl(m):
            if check is not None and not check(m.group(0)):
                return m.group(0)
            counts[label] = counts.get(label, 0) + 1
            return f"[{label}]"

        text = re.sub(pattern, repl, text)

    sub(r"\b(?:\d[ -]?){12,18}\d\b", "CARD", lambda s: luhn_valid(re.sub(r"\D", "", s)))
    sub(r"\b\d{3}-\d{2}-\d{4}\b", "SSN")
    sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "EMAIL")
    sub(r"\b\d{3}[-. ]\d{3}[-. ]\d{4}\b", "PHONE")
    return text, counts
