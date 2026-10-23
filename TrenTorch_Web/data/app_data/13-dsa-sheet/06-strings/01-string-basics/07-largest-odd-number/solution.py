def largest_odd_number(num):
    for i in range(len(num) - 1, -1, -1):
        if num[i] in "13579":
            return num[: i + 1]
    return ""
