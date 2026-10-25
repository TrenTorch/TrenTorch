def furthest_building(heights, bricks, ladders):
    best = 0
    for end in range(1, len(heights)):
        climbs = sorted(
            (
                heights[i] - heights[i - 1]
                for i in range(1, end + 1)
                if heights[i] > heights[i - 1]
            ),
            reverse=True,
        )
        if sum(climbs[ladders:]) <= bricks:
            best = end
        else:
            break
    return best
