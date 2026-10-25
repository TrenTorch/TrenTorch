def sort_by_frequency(s):
    chars = sorted(set(s), key=lambda ch: (-s.count(ch), ch))
    out = ""
    for ch in chars:
        out += ch * s.count(ch)
    return out
