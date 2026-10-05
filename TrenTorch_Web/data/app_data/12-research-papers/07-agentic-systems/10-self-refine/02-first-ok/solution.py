def first_ok_index(feedbacks):
    for i, f in enumerate(feedbacks):
        if f == "OK":
            return i
    return None
