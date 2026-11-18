def min_arrows(points):
    arrows = 0
    arrow = None
    for start, end in sorted(points, key=lambda p: p[1]):
        if arrow is None or start > arrow:
            arrows += 1
            arrow = end
    return arrows
