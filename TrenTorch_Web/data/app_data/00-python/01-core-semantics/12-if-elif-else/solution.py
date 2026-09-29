def classify_number(x: int | float) -> str:
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    elif x <= 10:
        return "small"
    else:
        return "large"
