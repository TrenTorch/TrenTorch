from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root):
    out = []
    queue = deque([root] if root else [])
    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            last = node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        out.append(last)
    return out
