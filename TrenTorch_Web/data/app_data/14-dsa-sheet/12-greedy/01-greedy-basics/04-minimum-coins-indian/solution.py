def fewest_notes(amount):
    total = 0
    for value in (2000, 500, 100, 50, 20, 10, 5, 2, 1):
        count, amount = divmod(amount, value)
        total += count
    return total
