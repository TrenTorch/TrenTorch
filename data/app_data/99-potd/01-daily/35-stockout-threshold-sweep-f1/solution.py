def best_f1_threshold(scores: list[float], y: list[int]) -> tuple[float, float]:
    total_positives = sum(y)
    order = sorted(range(len(scores)), key=lambda i: -scores[i])

    best_threshold = None
    best_f1 = -1.0
    tp = 0
    fp = 0

    i = 0
    n = len(order)
    while i < n:
        threshold = scores[order[i]]
        # Include every row tied at this exact score before evaluating.
        j = i
        while j < n and scores[order[j]] == threshold:
            idx = order[j]
            if y[idx] == 1:
                tp += 1
            else:
                fp += 1
            j += 1

        fn = total_positives - tp
        if tp + fp > 0 and tp + fn > 0:
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            if precision + recall > 0:
                f1 = 2 * precision * recall / (precision + recall)
                if f1 > best_f1:
                    best_f1 = f1
                    best_threshold = threshold

        i = j

    return best_threshold, best_f1
