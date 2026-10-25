def letter_combinations(digits):
    keys = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }
    if not digits:
        return []
    out = []

    def go(i, prefix):
        if i == len(digits):
            out.append(prefix)
            return
        for letter in keys[digits[i]]:
            go(i + 1, prefix + letter)

    go(0, "")
    return out
