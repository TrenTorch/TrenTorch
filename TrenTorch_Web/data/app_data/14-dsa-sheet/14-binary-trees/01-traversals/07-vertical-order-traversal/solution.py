from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def vertical_order(root):
    if not root:
        return []
    columns = {}
    queue = deque([(root, 0, 0)])
    while queue:
        node, row, col = queue.popleft()
        columns.setdefault(col, []).append((row, node.val))
        if node.left:
            queue.append((node.left, row + 1, col - 1))
        if node.right:
            queue.append((node.right, row + 1, col + 1))
    return [[v for _, v in sorted(columns[c])] for c in sorted(columns)]
