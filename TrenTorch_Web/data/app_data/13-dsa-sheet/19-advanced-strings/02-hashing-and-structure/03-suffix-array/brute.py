def suffix_array(s):
    return sorted(range(len(s)), key=lambda i: s[i:])
