from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def width_of_tree(root):
    if root is None:
        return 0
    best = 0
    queue = deque([(root, 0)])
    while queue:
        first = queue[0][1]
        last = first
        for _ in range(len(queue)):
            node, index = queue.popleft()
            last = index
            if node.left:
                queue.append((node.left, 2 * index + 1))
            if node.right:
                queue.append((node.right, 2 * index + 2))
        best = max(best, last - first + 1)
    return best
