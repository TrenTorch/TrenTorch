def analyze_route(points: list) -> tuple:
    """
    `points` is a list of (x, y) tuples of ints, in the order
    the route visits them. Return a 5-element tuple:

      (visit_counts, bounding_box, path_length,
       net_displacement, revisit_count)

    where:
      - visit_counts: a dictionary mapping each distinct
        (x, y) tuple to how many times it appears in `points`.
      - bounding_box: a tuple ((min_x, min_y), (max_x, max_y))
        covering all points. Compute it with a loop and
        comparisons (do not use min() or max()).
      - path_length: the sum of the Manhattan distances between
        each consecutive pair of points. Use an index loop.
      - net_displacement: the Manhattan distance between the
        first and last point. Obtain the first and last points
        with extended unpacking: first, *_, last = points
        (handle a single-point route separately).
      - revisit_count: len(points) minus the number of distinct
        points, i.e. how many visits were to a point already
        seen.

    An empty `points` returns ({}, None, 0, 0, 0).
    A single point returns:
      ({point: 1}, (point, point), 0, 0, 0)

    `points` and its tuples must not be modified.
    """
    pass
