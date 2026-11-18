def cheapest_price(n, flights, src, dst, k):
    best = None

    def walk(city, flights_used, cost):
        nonlocal best
        if city == dst and (best is None or cost < best):
            best = cost
        if flights_used == k + 1:
            return
        for a, b, price in flights:
            if a == city:
                walk(b, flights_used + 1, cost + price)

    walk(src, 0, 0)
    return best if best is not None else -1
