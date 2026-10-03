def injection_score(text, patterns):
    low = text.lower()
    return float(sum(w * low.count(p) for p, w in patterns.items()))


def screen_untrusted(text, patterns, threshold):
    low = text.lower()
    matched = sorted(p for p in patterns if p in low)
    return injection_score(text, patterns) >= threshold, matched
