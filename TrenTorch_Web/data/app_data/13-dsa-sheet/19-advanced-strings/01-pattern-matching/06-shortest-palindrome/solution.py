def shortest_palindrome(s):
    t = s + "#" + s[::-1]
    pi = [0] * len(t)
    k = 0
    for i in range(1, len(t)):
        while k and t[i] != t[k]:
            k = pi[k - 1]
        if t[i] == t[k]:
            k += 1
        pi[i] = k
    border = pi[-1] if t else 0
    return s[border:][::-1] + s
