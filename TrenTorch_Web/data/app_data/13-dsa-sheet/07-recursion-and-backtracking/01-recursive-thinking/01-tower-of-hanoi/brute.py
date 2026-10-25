def tower_of_hanoi(n):
    pegs = {1: list(range(n, 0, -1)), 2: [], 3: []}
    moves = []
    # iterative solution: the smallest disk moves in a fixed cycle; the other move is forced
    cycle = [(1, 2), (2, 3), (3, 1)] if n % 2 == 0 else [(1, 3), (3, 2), (2, 1)]
    small_at = 1
    steps = 2**n - 1
    for step in range(steps):
        if step % 2 == 0:
            src, dst = next(pair for pair in cycle if pair[0] == small_at)
        else:
            a, b = [p for p in (1, 2, 3) if p != small_at]
            if not pegs[a] or (pegs[b] and pegs[b][-1] < pegs[a][-1]):
                src, dst = b, a
            else:
                src, dst = a, b
        pegs[dst].append(pegs[src].pop())
        moves.append([src, dst])
        if step % 2 == 0:
            small_at = dst
    return moves
