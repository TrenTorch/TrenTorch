def cost_per_success(costs, successes):
    wins = sum(1 for s in successes if s)
    return sum(costs) / wins if wins else float("inf")


def pareto_front(points):
    front = []
    for i, (ci, ri) in enumerate(points):
        dominated = any(
            cj <= ci and rj >= ri and (cj < ci or rj > ri)
            for j, (cj, rj) in enumerate(points) if j != i
        )
        if not dominated:
            front.append(i)
    return front
