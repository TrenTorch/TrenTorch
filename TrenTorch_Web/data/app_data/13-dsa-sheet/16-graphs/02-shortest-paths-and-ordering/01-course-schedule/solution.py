from collections import deque


def can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    for course, pre in prerequisites:
        adj[pre].append(course)
        in_degree[course] += 1
    queue = deque(v for v in range(num_courses) if in_degree[v] == 0)
    taken = 0
    while queue:
        node = queue.popleft()
        taken += 1
        for nxt in adj[node]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)
    return taken == num_courses
