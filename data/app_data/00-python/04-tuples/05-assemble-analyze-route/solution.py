def analyze_route(points: list) -> tuple:
    if len(points) == 0:
        return ({}, None, 0, 0, 0)

    visit_counts = {}
    for point in points:
        if point in visit_counts:
            visit_counts[point] += 1
        else:
            visit_counts[point] = 1

    min_x = min_y = max_x = max_y = None
    for x, y in points:
        if min_x is None or x < min_x:
            min_x = x
        if max_x is None or x > max_x:
            max_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y
    bounding_box = ((min_x, min_y), (max_x, max_y))

    path_length = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        path_length += abs(x2 - x1) + abs(y2 - y1)

    if len(points) == 1:
        net_displacement = 0
    else:
        first, *_, last = points
        x1, y1 = first
        x2, y2 = last
        net_displacement = abs(x2 - x1) + abs(y2 - y1)

    revisit_count = len(points) - len(visit_counts)

    return (visit_counts, bounding_box, path_length, net_displacement, revisit_count)
