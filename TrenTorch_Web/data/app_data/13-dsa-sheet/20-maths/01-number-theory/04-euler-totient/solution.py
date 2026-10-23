def euler_phi(n):
    result = n
    d = 2
    while d * d <= n:
        if n % d == 0:
            while n % d == 0:
                n //= d
            result -= result // d
        d += 1 if d == 2 else 2
    if n > 1:
        result -= result // n
    return result
