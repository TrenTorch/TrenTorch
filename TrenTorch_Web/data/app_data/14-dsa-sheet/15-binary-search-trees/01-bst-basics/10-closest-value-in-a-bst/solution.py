class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def closest_value(root, target):
    best = root.val
    node = root
    while node:
        if (abs(node.val - target), node.val) < (abs(best - target), best):
            best = node.val
        node = node.left if target < node.val else node.right
    return best
