def classify_failures(failures: list[str], categories: dict[str, list[str]]) -> dict[str, int]:
    counts = {category: 0 for category in categories}
    counts["UNCATEGORIZED"] = 0
    for failure in failures:
        for category, keywords in categories.items():
            if any(keyword in failure for keyword in keywords):
                counts[category] += 1
                break
        else:
            counts["UNCATEGORIZED"] += 1
    return counts
