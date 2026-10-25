def palindrome_partitions(s):
    out = []

    def go(start, pieces):
        if start == len(s):
            out.append(list(pieces))
            return
        for j in range(start + 1, len(s) + 1):
            piece = s[start:j]
            if piece == piece[::-1]:
                pieces.append(piece)
                go(j, pieces)
                pieces.pop()

    go(0, [])
    return sorted(out)
