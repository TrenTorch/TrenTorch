def restore_ip_addresses(s):
    out = []

    def valid(part):
        return (part == "0" or not part.startswith("0")) and int(part) <= 255

    def go(start, parts):
        if len(parts) == 4:
            if start == len(s):
                out.append(".".join(parts))
            return
        for length in (1, 2, 3):
            part = s[start : start + length]
            if len(part) == length and valid(part):
                go(start + length, parts + [part])

    go(0, [])
    return sorted(out)
