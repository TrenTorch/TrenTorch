def largest_odd_number(num):
    best = ""
    for i in range(len(num)):
        for j in range(i + 1, len(num) + 1):
            part = num[i:j]
            if int(part[-1]) % 2 == 1 and (len(part), part) > (len(best), best):
                best = part
    return best
