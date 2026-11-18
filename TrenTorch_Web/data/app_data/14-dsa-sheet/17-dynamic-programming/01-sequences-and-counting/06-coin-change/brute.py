from collections import deque


def coin_change(coins, amount):
    if amount == 0:
        return 0
    seen = {0}
    queue = deque([(0, 0)])
    while queue:
        total, used = queue.popleft()
        for c in coins:
            nxt = total + c
            if nxt == amount:
                return used + 1
            if nxt < amount and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, used + 1))
    return -1
