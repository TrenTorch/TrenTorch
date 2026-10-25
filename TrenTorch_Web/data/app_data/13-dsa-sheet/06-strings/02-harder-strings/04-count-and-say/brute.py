def count_and_say(n):
    term = "1"
    for _ in range(n - 1):
        out = ""
        i = 0
        while i < len(term):
            j = i
            while j < len(term) and term[j] == term[i]:
                j += 1
            out += str(j - i) + term[i]
            i = j
        term = out
    return term
