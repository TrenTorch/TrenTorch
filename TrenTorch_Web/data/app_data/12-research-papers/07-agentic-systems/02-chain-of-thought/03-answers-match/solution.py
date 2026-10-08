def answers_match(pred, gold):
    def norm(s):
        return s.replace(",", "").strip().lower()

    p, g = norm(pred), norm(gold)
    try:
        return abs(float(p) - float(g)) < 1e-6
    except ValueError:
        return p == g
