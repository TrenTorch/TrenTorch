def cycles_total(T0, Tmult, n):
    total = 0
    T_i = T0
    for _ in range(n):
        total += T_i
        T_i *= Tmult
    return total
