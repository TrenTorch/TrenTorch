import re


def normalize_text(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
