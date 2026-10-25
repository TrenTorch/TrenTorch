def daily_temperatures(temps):
    out = []
    for i in range(len(temps)):
        out.append(
            next((j - i for j in range(i + 1, len(temps)) if temps[j] > temps[i]), 0)
        )
    return out
