from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def distance_k(root, target, k):
    parent = {}
    start = None
    stack = [(root, None)]
    while stack:
        node, par = stack.pop()
        parent[node] = par
        if node.val == target:
            start = node
        if node.left:
            stack.append((node.left, node))
        if node.right:
            stack.append((node.right, node))
    seen = {start}
    frontier = deque([start])
    for _ in range(k):
        for _ in range(len(frontier)):
            node = frontier.popleft()
            for nxt in (node.left, node.right, parent[node]):
                if nxt and nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
    return sorted(node.val for node in frontier)
