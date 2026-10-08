def recency_score(hours, decay=0.995):
    return decay**hours
