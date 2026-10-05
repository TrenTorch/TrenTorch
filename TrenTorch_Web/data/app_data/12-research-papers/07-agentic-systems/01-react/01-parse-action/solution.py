import re


def parse_action(text):
    m = re.search(r"Action:\s*(\w+)\[(.*?)\]", text)
    return (m.group(1), m.group(2)) if m else None
