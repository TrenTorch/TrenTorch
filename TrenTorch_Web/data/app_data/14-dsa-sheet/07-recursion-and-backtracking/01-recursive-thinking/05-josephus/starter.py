from collections import deque


def josephus(n: int, k: int) -> int:
    """Return the number of the survivor."""
    # This is correct but too slow: it walks around the circle for every removal.
    people = deque(range(1, n + 1))
    while len(people) > 1:
        for _ in range((k - 1) % len(people)):
            people.append(people.popleft())
        people.popleft()
    return people[0]
