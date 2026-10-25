from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def burn_time(root, start):
    parent = {}
    origin = None
    stack = [(root, None)]
    while stack:
        node, par = stack.pop()
        parent[node] = par
        if node.val == start:
            origin = node
        if node.left:
            stack.append((node.left, node))
        if node.right:
            stack.append((node.right, node))
    seen = {origin}
    frontier = deque([origin])
    minutes = -1
    while frontier:
        minutes += 1
        for _ in range(len(frontier)):
            node = frontier.popleft()
            for nxt in (node.left, node.right, parent[node]):
                if nxt and nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
    return minutes
