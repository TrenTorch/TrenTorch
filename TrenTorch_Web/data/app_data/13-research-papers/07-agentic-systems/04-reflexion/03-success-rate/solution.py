def success_rate(results):
    if not results:
        return 0.0
    return sum(bool(r) for r in results) / len(results)
