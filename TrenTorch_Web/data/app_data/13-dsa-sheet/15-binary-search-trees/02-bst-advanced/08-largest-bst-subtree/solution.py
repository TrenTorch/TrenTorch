class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def largest_bst_subtree(root):
    best = 0
    inf = float("inf")

    def go(node):
        nonlocal best
        if node is None:
            return 0, inf, -inf
        left_size, left_low, left_high = go(node.left)
        right_size, right_low, right_high = go(node.right)
        if left_size >= 0 and right_size >= 0 and left_high < node.val < right_low:
            size = left_size + right_size + 1
            best = max(best, size)
            return size, min(left_low, node.val), max(right_high, node.val)
        return -1, -inf, inf

    go(root)
    return best
